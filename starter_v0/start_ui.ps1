param([int]$Port = 8000)

$ErrorActionPreference = "Stop"

$scriptPath = $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
$uiDir = Join-Path $projectRoot "ui"

Write-Host "Project root: $projectRoot" -ForegroundColor Cyan

$venvPython = Join-Path $projectRoot ".venv" "Scripts" "python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: .venv not found. Run: python -m venv .venv" -ForegroundColor Red
    exit 1
}

$tempUi = Join-Path $env:TEMP "research_agent_ui"
if (Test-Path $tempUi) { Remove-Item $tempUi -Recurse -Force }
New-Item -ItemType Directory -Path $tempUi -Force | Out-Null
Copy-Item -Path "$uiDir\*" -Destination $tempUi -Recurse -Force

# Write wrapper CMD for shell_exec (must avoid Unicode paths in command line)
$wrapper = Join-Path $tempUi "run_bridge.cmd"
@'
@echo off
setlocal enabledelayedexpansion
set PYTHONIOENCODING=utf-8
set "PYTHON=%PROJECT_ROOT%\.venv\Scripts\python.exe"
set "BRIDGE=%~dp0bridge.py"
"%PYTHON%" "%BRIDGE%" --message "%~1"
endlocal
'@ | Out-File -FilePath $wrapper -Encoding ascii

# Remove old router and debug files from temp (if any)
Get-ChildItem $tempUi -Filter "*.php" | Where-Object { $_.Name -match '^(debug|test|router)' } | Remove-Item -Force

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Research Agent Chat UI" -ForegroundColor Green
Write-Host "  URL: http://127.0.0.1:$Port" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop." -ForegroundColor Gray

$env:PROJECT_ROOT = $projectRoot
Start-Process "http://127.0.0.1:$Port"
& "C:\xampp\php\php.exe" "-S" "127.0.0.1:$Port" "-t" $tempUi
