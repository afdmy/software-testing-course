"""以课程测试用例清单中的中文标题运行全部自动化测试。"""

import re
import sys
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
sys.path.insert(0, str(TEST_DIR))

from case_names import CASE_NAMES


class ChineseTextTestResult(unittest.TextTestResult):
    def getDescription(self, test):
        match = re.search(r"test_tc(\d{3})_", test.id(), re.IGNORECASE)
        if not match:
            return test.id()
        case_id = f"TC{match.group(1)}"
        return f"{case_id} {CASE_NAMES.get(case_id, test.id())}"


def main():
    print("SkyGuard 模块一自动化测试")
    print("开始执行 40 条测试用例\n")
    discovered = unittest.defaultTestLoader.discover(
        start_dir=str(TEST_DIR), pattern="test_*.py", top_level_dir=str(PROJECT_ROOT)
    )
    def flatten(items):
        for item in items:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item

    def case_number(test):
        match = re.search(r"test_tc(\d{3})_", test.id(), re.IGNORECASE)
        return int(match.group(1)) if match else 9999

    suite = unittest.TestSuite(sorted(flatten(discovered), key=case_number))
    result = unittest.TextTestRunner(
        verbosity=2, resultclass=ChineseTextTestResult, stream=sys.stdout
    ).run(suite)
    print("\n执行汇总")
    print(f"用例总数：{result.testsRun}")
    print(f"通过数量：{result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"失败数量：{len(result.failures) + len(result.errors)}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
