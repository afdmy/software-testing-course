import asyncio
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

import result_paths
import visualization_api


class VisualizationApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.roots_patch = patch.object(result_paths, "RESULTS_ROOTS", (self.root,))
        self.roots_patch.start()

    def tearDown(self):
        self.roots_patch.stop()
        self.temp.cleanup()

    def task(self, group="adversarial_results", task_id="task-1"):
        path = self.root / group / task_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def run_async(self, coro):
        return asyncio.run(coro)

    def test_tc009_results_unknown_task_returns_404(self):
        with self.assertRaises(HTTPException) as ctx:
            self.run_async(visualization_api.get_task_results("missing"))
        self.assertEqual(ctx.exception.status_code, 404)

    def test_tc010_results_empty_task_returns_empty_images(self):
        self.task()
        data = self.run_async(visualization_api.get_task_results("task-1"))
        self.assertEqual(data["images"], [])
        self.assertEqual(data["metadata"]["task_kind"], "training_or_metrics_only")

    def test_tc011_results_reads_root_png(self):
        (self.task() / "sample.png").write_bytes(b"png")
        data = self.run_async(visualization_api.get_task_results("task-1"))
        self.assertEqual(data["images"][0]["path"], "sample.png")

    def test_tc012_results_recursively_reads_nested_jpg(self):
        nested = self.task() / "original" / "batch-a"
        nested.mkdir(parents=True)
        (nested / "uav.jpg").write_bytes(b"jpg")
        data = self.run_async(visualization_api.get_task_results("task-1"))
        self.assertEqual(data["images"][0]["path"], "original/batch-a/uav.jpg")

    def test_tc013_results_url_uses_forward_slashes(self):
        nested = self.task() / "comparison"
        nested.mkdir()
        (nested / "a.jpg").write_bytes(b"jpg")
        data = self.run_async(visualization_api.get_task_results("task-1"))
        self.assertNotIn("\\\\", data["images"][0]["url"])
        self.assertIn("comparison/a.jpg", data["images"][0]["url"])

    def test_tc014_results_url_encodes_space(self):
        (self.task() / "a b.png").write_bytes(b"png")
        data = self.run_async(visualization_api.get_task_results("task-1"))
        self.assertIn("a%20b.png", data["images"][0]["url"])

    def test_tc015_results_classifies_nested_image_by_first_folder(self):
        nested = self.task() / "adversarial"
        nested.mkdir()
        (nested / "a.bmp").write_bytes(b"bmp")
        data = self.run_async(visualization_api.get_task_results("task-1"))
        self.assertEqual(data["images"][0]["type"], "adversarial")

    def test_tc016_results_ignores_unsupported_extension(self):
        (self.task() / "note.txt").write_text("x", encoding="utf-8")
        data = self.run_async(visualization_api.get_task_results("task-1"))
        self.assertEqual(data["images"], [])

    def test_tc017_results_reads_progress_json(self):
        (self.task() / "progress.json").write_text(json.dumps({"status": "completed", "metrics": {"rate": 0.8}}), encoding="utf-8")
        data = self.run_async(visualization_api.get_task_results("task-1"))
        self.assertEqual(data["metrics"]["progress"]["status"], "completed")

    def test_tc018_results_preserves_task_group_metadata(self):
        (self.task() / "metadata.json").write_text(json.dumps({"owner": "local"}), encoding="utf-8")
        data = self.run_async(visualization_api.get_task_results("task-1"))
        self.assertEqual(data["metadata"]["task_group"], "attack")
        self.assertEqual(data["metadata"]["owner"], "local")

    def test_tc019_image_path_traversal_is_rejected(self):
        self.task()
        with self.assertRaises(HTTPException) as ctx:
            self.run_async(visualization_api.get_result_image("task-1", "../secret.png"))
        self.assertEqual(ctx.exception.status_code, 400)

    def test_tc020_existing_image_returns_file_response(self):
        img = self.task() / "original" / "uav.jpg"
        img.parent.mkdir()
        img.write_bytes(b"jpg")
        response = self.run_async(visualization_api.get_result_image("task-1", "original/uav.jpg"))
        self.assertEqual(Path(response.path), img)

    def test_tc021_latest_task_skips_directory_without_images(self):
        old = self.task(task_id="with-image")
        (old / "a.jpg").write_bytes(b"jpg")
        empty = self.task(task_id="new-empty")
        os.utime(old, (100, 100)); os.utime(empty, (200, 200))
        data = self.run_async(visualization_api.get_latest_task())
        self.assertEqual(data["task_id"], "with-image")

    def test_tc022_recent_tasks_limit_lower_boundary(self):
        for i in range(3):
            path = self.task(task_id=f"task-{i}")
            os.utime(path, (100 + i, 100 + i))
        data = self.run_async(visualization_api.get_recent_tasks(0))
        self.assertEqual(len(data), 1)

    def test_tc023_recent_tasks_limit_upper_boundary(self):
        for i in range(102):
            self.task(task_id=f"task-{i:03d}")
        data = self.run_async(visualization_api.get_recent_tasks(101))
        self.assertEqual(len(data), 100)

    def test_tc024_recent_tasks_sorted_newest_first(self):
        for name, stamp in (("old", 100), ("new", 300), ("middle", 200)):
            path = self.task(task_id=name)
            os.utime(path, (stamp, stamp))
        data = self.run_async(visualization_api.get_recent_tasks(3))
        self.assertEqual([x["task_id"] for x in data], ["new", "middle", "old"])


if __name__ == "__main__":
    unittest.main()
