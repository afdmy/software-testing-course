$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot
$env:PYTHONUTF8 = '1'
Write-Host '当前模式：修复后回归，预期 40 条全部通过'
conda run --no-capture-output -n skyguard python module1_tests\run_all.py --phase regression
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
