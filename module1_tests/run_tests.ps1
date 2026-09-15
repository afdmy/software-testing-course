$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot
$env:PYTHONUTF8 = '1'
Write-Host '当前模式：首次缺陷发现，预期 36 条通过、4 条失败'
conda run --no-capture-output -n skyguard python module1_tests\run_all.py --phase discovery
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
