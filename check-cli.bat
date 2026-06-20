@echo off
:: Lightweight launcher for development/use from the repo root
cd /d "%~dp0"

:: Try py launcher first (most reliable on Windows)
where py >nul 2>&1
if not errorlevel 1 (
    py -m multiformat_validator %*
    exit /b %ERRORLEVEL%
)

:: Try system python
where python >nul 2>&1
if not errorlevel 1 (
    python -m multiformat_validator %*
    exit /b %ERRORLEVEL%
)

:: Try python3
where python3 >nul 2>&1
if not errorlevel 1 (
    python3 -m multiformat_validator %*
    exit /b %ERRORLEVEL%
)

:: Fall back to venv python if available
if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" -m multiformat_validator %*
    exit /b %ERRORLEVEL%
)

echo [!] Python not found. Install Python 3.12+ or run install.bat first.
exit /b 1
