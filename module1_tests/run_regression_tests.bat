@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0.."
set PYTHONUTF8=1
conda run --no-capture-output -n skyguard python module1_tests\run_all.py --phase regression
exit /b %errorlevel%
