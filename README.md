# software-testing-course

SkyGuard UAV Defense 软件质量测试课程实践项目，包含平台源码、模块一自动化测试工程和课程交付文档。

## 项目结构

- `backend/`：FastAPI、Celery、攻击、防御与结果可视化后端源码
- `frontend/`：React + Vite 前端源码
- `airsim/`：AirSim 联调相关代码
- `module1_tests/`：植入项目根目录的模块一自动化测试工程
- `SkyGuard_模块一_自动化测试工程/`：课程交付版自动化测试工程
- `SkyGuard_Windows_Setup.md`：Windows 环境启动说明
- `SkyGuard_README.md`：原项目详细说明

数据集、模型训练结果、攻击结果、`node_modules` 和模型权重未提交到仓库，需按启动说明自行准备。

## 测试范围

40条自动化用例覆盖结果路径、可视化结果接口、任务进度接口和关键前端交互契约。快速测试不加载YOLO模型、不访问GPU，也不修改已有业务结果；真实PGD攻击、模型训练和AirSim联调需要单独执行。

## 首次缺陷发现

在项目根目录执行：

```bat
module1_tests\run_tests.bat
```

预期结果为40条用例中36条通过、4条失败，通过率90%。4条失败用例用于复现并关联SG-001至SG-004，因此脚本退出码为1属于预期结果。

## 修复后回归

```bat
module1_tests\run_regression_tests.bat
```

预期结果为40条全部通过、0条失败，通过率100%，脚本退出码为0。控制台中的`TCxxx`编号和中文名称与测试用例清单一一对应。
