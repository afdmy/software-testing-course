import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FrontendContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dashboard = (ROOT / "frontend/src/pages/Dashboard.jsx").read_text(encoding="utf-8")
        cls.defense = (ROOT / "frontend/src/pages/DefenseScenarios.jsx").read_text(encoding="utf-8")
        cls.vite = (ROOT / "frontend/vite.config.js").read_text(encoding="utf-8")
        cls.tasks = (ROOT / "backend/tasks.py").read_text(encoding="utf-8")

    def test_tc033_start_drill_button_has_attack_route(self):
        self.assertIn("onClick={() => navigate('/attack-scenarios')}", self.dashboard)

    def test_tc034_report_button_has_report_route(self):
        self.assertIn("onClick={() => navigate('/reports')}", self.dashboard)

    def test_tc035_dashboard_imports_use_navigate(self):
        self.assertIn("useNavigate", self.dashboard)

    def test_tc036_scenarios_proxy_is_configured(self):
        self.assertIn("'/scenarios':", self.vite)

    def test_tc037_visualization_proxy_is_configured(self):
        self.assertIn("'/visualization/':", self.vite)

    def test_tc038_defense_uses_auto_device(self):
        self.assertIn("device: 'auto'", self.defense)

    def test_tc039_defense_formats_object_errors(self):
        self.assertIn("const formatError", self.defense)
        self.assertIn("JSON.stringify", self.defense)

    def test_tc040_worker_subprocess_uses_utf8(self):
        self.assertIn("encoding=\"utf-8\"", self.tasks)
        self.assertIn("errors=\"replace\"", self.tasks)


if __name__ == "__main__":
    unittest.main()
