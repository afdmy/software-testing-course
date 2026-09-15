# SkyGuard 模块一自动化测试工程

本工程用于 SkyGuard 模块一自动化测试，覆盖结果路径、可视化结果接口、任务进度接口和关键前端交互契约。测试不加载 YOLO 模型、不访问 GPU，也不会修改现有业务结果；文件类测试只在临时目录中运行。

## 环境

- Windows 10/11
- Conda 环境 `skyguard`
- Python 3.10 或项目当前兼容版本
- 已安装项目后端依赖（FastAPI 等）

## 首次缺陷发现结果

在资源管理器中双击 `run_tests.bat`，或在 PowerShell 中执行：

```powershell
.\module1_tests\run_tests.ps1
```

该入口重放修复前的四个缺陷证据。总计 40 条，其中 36 条通过、4 条失败，通过率 90%。失败用例为 TC013、TC033、TC038 和 TC039。

## 修复后回归

双击 `run_regression_tests.bat`，或在 PowerShell 中执行：

```powershell
.\module1_tests\run_regression_tests.ps1
```

等价命令：

```powershell
conda run --no-capture-output -n skyguard python module1_tests\run_all.py --phase regression
```

修复后回归结果为 40 条全部通过。退出码为 0 表示全部通过，非 0 表示至少一个用例失败。命令行显示的 `TCxxx` 编号和中文名称与 Excel 测试用例清单一一对应。

## 覆盖范围

- `test_result_paths.py`：规范结果目录、旧目录兼容和查找优先级。
- `test_visualization_api.py`：图片递归发现、URL、指标、边界值和路径穿越防护。
- `test_progress_api.py`：四类任务进度落盘、时间戳、内存与磁盘读取。
- `test_frontend_contracts.py`：首页按钮路由、代理配置、CPU 自动选择和对象错误格式化。

## 限制

这些测试属于稳定、可重复执行的接口和契约测试。真实 PGD 攻击、YOLO 推理、对抗训练和 AirSim 联调耗时长且依赖数据、模型、Redis/Celery 或仿真器，应作为人工系统测试单独执行并保留截图或日志。
