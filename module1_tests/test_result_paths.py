import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

import result_paths


class ResultPathTests(unittest.TestCase):
    def test_tc001_primary_root_is_backend_results(self):
        self.assertEqual(result_paths.PRIMARY_RESULTS_ROOT, BACKEND / "results")

    def test_tc002_legacy_root_is_project_results(self):
        self.assertEqual(result_paths.LEGACY_RESULTS_ROOT, ROOT / "results")

    def test_tc003_result_path_without_task(self):
        self.assertEqual(result_paths.result_path("evaluation_results"), BACKEND / "results" / "evaluation_results")

    def test_tc004_result_path_with_task(self):
        self.assertEqual(result_paths.result_path("adversarial_results", "task-a"), BACKEND / "results" / "adversarial_results" / "task-a")

    def test_tc005_find_task_prefers_primary_root(self):
        with tempfile.TemporaryDirectory() as p, tempfile.TemporaryDirectory() as l:
            primary, legacy = Path(p), Path(l)
            (primary / "adversarial_results" / "same").mkdir(parents=True)
            (legacy / "adversarial_results" / "same").mkdir(parents=True)
            with patch.object(result_paths, "RESULTS_ROOTS", (primary, legacy)):
                group, path = result_paths.find_task_dir("same")
            self.assertEqual((group, path), ("adversarial_results", primary / "adversarial_results" / "same"))

    def test_tc006_find_task_falls_back_to_legacy_root(self):
        with tempfile.TemporaryDirectory() as p, tempfile.TemporaryDirectory() as l:
            primary, legacy = Path(p), Path(l)
            expected = legacy / "defense_results" / "legacy-task"
            expected.mkdir(parents=True)
            with patch.object(result_paths, "RESULTS_ROOTS", (primary, legacy)):
                group, path = result_paths.find_task_dir("legacy-task")
            self.assertEqual((group, path), ("defense_results", expected))

    def test_tc007_find_task_returns_none_for_unknown_task(self):
        with tempfile.TemporaryDirectory() as p:
            with patch.object(result_paths, "RESULTS_ROOTS", (Path(p),)):
                self.assertEqual(result_paths.find_task_dir("missing"), (None, None))

    def test_tc008_find_task_respects_group_filter(self):
        with tempfile.TemporaryDirectory() as p:
            root = Path(p)
            (root / "defense_results" / "only-defense").mkdir(parents=True)
            with patch.object(result_paths, "RESULTS_ROOTS", (root,)):
                self.assertEqual(result_paths.find_task_dir("only-defense", ["adversarial_results"]), (None, None))


if __name__ == "__main__":
    unittest.main()
