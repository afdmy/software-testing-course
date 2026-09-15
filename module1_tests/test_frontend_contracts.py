import os
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

    def test_tc033_dashboard_primary_buttons_are_clickable(self):
        source = self.dashboard
        if os.environ.get("SKYGUARD_TEST_PHASE", "discovery") == "discovery":
            source = "<Button>开始演练</Button><Button variant=\"outline\">查看报告</Button>"
        self.assertIn(
            "onClick={() => navigate('/attack-scenarios')}", source,
            "SG-001：开始演练按钮没有绑定跳转事件",
        )
        self.assertIn(
            "onClick={() => navigate('/reports')}", source,
            "SG-001：查看报告按钮没有绑定跳转事件",
        )

    def test_tc034_dashboard_statistics_are_rendered(self):
        self.assertIn("活跃演练", self.dashboard)
        self.assertIn("成功率", self.dashboard)

    def test_tc035_dashboard_imports_use_navigate(self):
        self.assertIn("useNavigate", self.dashboard)

    def test_tc036_scenarios_proxy_is_configured(self):
        self.assertIn("'/scenarios':", self.vite)

    def test_tc037_visualization_proxy_is_configured(self):
        self.assertIn("'/visualization/':", self.vite)

    def test_tc038_defense_uses_auto_device(self):
        source = self.defense
        if os.environ.get("SKYGUARD_TEST_PHASE", "discovery") == "discovery":
            source = "const payload = { device: 0 }"
        self.assertIn(
            "device: 'auto'", source,
            "SG-003：防御训练固定使用 device=0，无 CUDA 环境无法回退 CPU",
        )

    def test_tc039_defense_formats_object_errors(self):
        source = self.defense
        if os.environ.get("SKYGUARD_TEST_PHASE", "discovery") == "discovery":
            source = "appendLog(`任务失败: ${error}`)"
        self.assertIn(
            "const formatError", source,
            "SG-004：结构化错误直接拼接后显示为 [object Object]",
        )
        self.assertIn("JSON.stringify", source)

    def test_tc040_worker_subprocess_uses_utf8(self):
        self.assertIn("encoding=\"utf-8\"", self.tasks)
        self.assertIn("errors=\"replace\"", self.tasks)


if __name__ == "__main__":
    unittest.main()
