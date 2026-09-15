$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot
$env:PYTHONUTF8 = '1'
conda run --no-capture-output -n skyguard python module1_tests\run_all.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
