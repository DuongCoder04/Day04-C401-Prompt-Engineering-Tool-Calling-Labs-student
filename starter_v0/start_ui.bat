@echo off
REM Start Research Agent Chat UI
REM Usage: start_ui.bat

setlocal enabledelayedexpansion

REM Find the project root (where this script is)
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%"

REM Remove trailing backslash
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

echo PROJECT_ROOT=%PROJECT_ROOT%

REM Check if .venv exists
if not exist "%PROJECT_ROOT%\.venv\Scripts\python.exe" (
    echo ERROR: .venv not found. Run: python -m venv .venv
    exit /b 1
)

REM Copy UI files to temp directory without Unicode chars
set "TEMP_UI=%TEMP%\research_agent_ui"
if exist "%TEMP_UI%" rmdir /s /q "%TEMP_UI%"
mkdir "%TEMP_UI%" 2>nul

xcopy /e /i /q "%PROJECT_ROOT%\ui\*" "%TEMP_UI%" >nul

echo Starting server at http://127.0.0.1:8000
echo Press Ctrl+C to stop.

REM Set env var and start PHP
set "PROJECT_ROOT=%PROJECT_ROOT%"
start "" http://127.0.0.1:8000
C:\xampp\php\php.exe -S 127.0.0.1:8000 -t "%TEMP_UI%"

endlocal
