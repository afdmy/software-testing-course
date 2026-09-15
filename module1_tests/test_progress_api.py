import asyncio
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

import progress_api
import result_paths


class ProgressApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.patch_roots = patch.object(result_paths, "RESULTS_ROOTS", (self.root,))
        self.patch_primary = patch.object(result_paths, "PRIMARY_RESULTS_ROOT", self.root)
        self.patch_roots.start(); self.patch_primary.start()
        progress_api.task_progress.clear()

    def tearDown(self):
        progress_api.task_progress.clear()
        self.patch_primary.stop(); self.patch_roots.stop(); self.temp.cleanup()

    def run_async(self, coro):
        return asyncio.run(coro)

    def update(self, task_id, data):
        with patch.object(progress_api.manager, "broadcast", new=AsyncMock()):
            return self.run_async(progress_api.update_progress(task_id, data))

    def test_tc025_update_attack_creates_adversarial_result(self):
        self.update("attack-1", {"attack_name": "pgd", "status": "running"})
        self.assertTrue((self.root / "adversarial_results" / "attack-1" / "progress.json").is_file())

    def test_tc026_update_defense_creates_defense_result(self):
        self.update("defense-1", {"defense_type": "adversarial_training", "status": "running"})
        self.assertTrue((self.root / "defense_results" / "defense-1" / "progress.json").is_file())

    def test_tc027_update_scenario_creates_scenario_result(self):
        self.update("scenario-1", {"task_group": "scenario", "status": "running"})
        self.assertTrue((self.root / "scenario_results" / "scenario-1" / "progress.json").is_file())

    def test_tc028_update_default_creates_evaluation_result(self):
        self.update("eval-1", {"status": "running"})
        self.assertTrue((self.root / "evaluation_results" / "eval-1" / "progress.json").is_file())

    def test_tc029_update_adds_iso_timestamp(self):
        payload = {"status": "running"}
        self.update("time-1", payload)
        self.assertIn("T", payload["timestamp"])

    def test_tc030_get_progress_prefers_memory(self):
        progress_api.task_progress["memory"] = {"status": "completed"}
        data = self.run_async(progress_api.get_progress("memory"))
        self.assertEqual(data["status"], "completed")

    def test_tc031_get_progress_reads_persisted_file(self):
        path = self.root / "evaluation_results" / "disk"
        path.mkdir(parents=True)
        (path / "progress.json").write_text(json.dumps({"status": "completed"}), encoding="utf-8")
        data = self.run_async(progress_api.get_progress("disk"))
        self.assertEqual(data["status"], "completed")

    def test_tc032_get_unknown_progress_returns_404(self):
        with self.assertRaises(HTTPException) as ctx:
            self.run_async(progress_api.get_progress("missing"))
        self.assertEqual(ctx.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
