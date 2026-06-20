@echo off
REM Installer for MultiFormat Validator CLI
cd /d "%~dp0"

REM If this script was launched in a non-CMD shell (PowerShell), re-run under cmd.exe.
REM CMDCMDLINE is present when running under cmd.exe. If absent, re-launch.
if not defined CMDCMDLINE (
    echo Detected non-CMD environment. Re-launching under cmd.exe...
    cmd /c ""%~f0" %*"
    exit /b %ERRORLEVEL%
)
cls
color 0B

echo.
echo ========================================
echo   MultiFormat Validator CLI - Setup
echo ========================================
echo.
echo   [1] Install
echo   [2] Uninstall
echo.

set "CHOICE="
set "AUTO_NOPROMPT=0"

rem Support unattended mode: pass --yes to auto-accept defaults
for %%A in (%*) do (
  if /I "%%~A"=="--yes" set "AUTO_NOPROMPT=1"
)

if "%AUTO_NOPROMPT%"=="1" (
  set "CHOICE=1"
) else (
  set /p "CHOICE=  Choose (1-2): "
)

if "%CHOICE%"=="1" goto :install
if "%CHOICE%"=="2" goto :uninstall
echo [!] Invalid choice.
pause
exit /b 1

:install
echo.
echo ========================================
echo   Installing...
echo ========================================
echo.

echo [1/6] Locating Python...

set "PYTHON_CMD="

REM 优先使用 py launcher
where py >nul 2>&1 && set "PYTHON_CMD=py"

REM 尝试 python 命令
if not defined PYTHON_CMD where python >nul 2>&1 && set "PYTHON_CMD=python"

REM 尝试 python3 命令
if not defined PYTHON_CMD where python3 >nul 2>&1 && set "PYTHON_CMD=python3"

REM 尝试本地 venv
if not defined PYTHON_CMD if exist ".venv\Scripts\python.exe" set "PYTHON_CMD=%~dp0.venv\Scripts\python.exe"

REM 尝试 Microsoft Store Python 路径
if not defined PYTHON_CMD (
    for /f "tokens=*" %%i in ('dir /b "%LOCALAPPDATA%\Packages\*Python*" 2^>nul') do (
        for /f "tokens=*" %%j in ('dir /b "%LOCALAPPDATA%\Packages\%%i\LocalCache\Local\Python*" 2^>nul') do (
            if exist "%LOCALAPPDATA%\Packages\%%i\LocalCache\Local\%%j\python.exe" (
                set "PYTHON_CMD=%LOCALAPPDATA%\Packages\%%i\LocalCache\Local\%%j\python.exe"
            )
        )
    )
)

if not defined PYTHON_CMD (
    echo [!] Python not found.
    echo [!] Please install Python 3.12+ from: https://www.python.org/downloads/
    echo [!] Or install from Microsoft Store.
    pause
    exit /b 1
)

echo [v] Using: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

echo [2/6] Ensuring pip...
%PYTHON_CMD% -m pip --version >nul 2>&1 || (
    echo [*] pip not found. Installing pip...
    %PYTHON_CMD% -m ensurepip --upgrade || (
        echo [!] Failed to ensure pip.
        pause
        exit /b 1
    )
)
echo [v] pip ready.
echo.

echo [3/6] Installing dependencies (colorama, pytest)...
%PYTHON_CMD% -m pip install "colorama>=0.4.6" --disable-pip-version-check >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Failed to install colorama.
    pause
    exit /b 1
)
echo [v] colorama installed.

%PYTHON_CMD% -m pip install "pytest>=7.0.0" --disable-pip-version-check >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Failed to install pytest.
    pause
    exit /b 1
)
echo [v] pytest installed.

%PYTHON_CMD% -m pip install pyyaml --disable-pip-version-check >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] pyyaml not installed. YAML support will be limited.
) else (
    echo [v] pyyaml installed.
)
echo.

echo [4/6] Installing package (editable)...
%PYTHON_CMD% -m pip install -e . --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [!] Package installation failed.
    pause
    exit /b 1
)
echo [v] Package installed.
echo.

echo [5/6] Select default language...
echo.

:: Force Python to use UTF-8 stdout so all languages display correctly
set "PYTHONIOENCODING=utf-8"

set "TMPPY=%TEMP%\_mfv_lang_select_%RANDOM%.py"
set "LANGTMP=%TEMP%\_mfv_lang_code_%RANDOM%.txt"
set "LANG_CODE=en"

if "%AUTO_NOPROMPT%"=="1" (
    set "LANG_CODE=en"
    goto :lang_done
)

echo lang_map = {"1": "zh_TW", "2": "zh_CN", "3": "en", "4": "ja", "5": "ko"} > "%TMPPY%"
echo labels = { >> "%TMPPY%"
echo     "1": ("\u7e41\u9ad4\u4e2d\u6587", "Traditional Chinese"), >> "%TMPPY%"
echo     "2": ("\u7b80\u4f53\u4e2d\u6587", "Simplified Chinese"), >> "%TMPPY%"
echo     "3": ("English", "English"), >> "%TMPPY%"
echo     "4": ("\u65e5\u672c\u8a9e", "Japanese"), >> "%TMPPY%"
echo     "5": ("\ud55c\uad6d\uc5b4", "Korean"), >> "%TMPPY%"
echo } >> "%TMPPY%"
echo print^(^) >> "%TMPPY%"
echo for k in sorted^(labels^): >> "%TMPPY%"
echo     cn, en = labels[k] >> "%TMPPY%"
echo     print^(f"  {k}. {cn} ({en})"^) >> "%TMPPY%"
echo print^(^) >> "%TMPPY%"
echo while True: >> "%TMPPY%"
echo     choice = input^("  Choose language [1-5, default=3]: "^).strip^(^) or "3" >> "%TMPPY%"
echo     if choice in lang_map: >> "%TMPPY%"
echo         with open^(r"%LANGTMP%", "w", encoding="utf-8"^) as f: >> "%TMPPY%"
echo             f.write^(lang_map[choice]^) >> "%TMPPY%"
echo         break >> "%TMPPY%"
echo     print^("  Invalid choice. Please enter 1-5."^) >> "%TMPPY%"

"%PYTHON_CMD%" "%TMPPY%"
if exist "%LANGTMP%" (
    set /p LANG_CODE=<"%LANGTMP%"
    del "%LANGTMP%" 2>nul
)
del "%TMPPY%" 2>nul

:lang_done
echo [v] Default language: %LANG_CODE%
echo.

echo [6/6] Saving config...
set "TMPPY=%TEMP%\_mfv_save_config_%RANDOM%.py"

echo from multiformat_validator.config import load_config, save_config > "%TMPPY%"
echo c = load_config^(^) >> "%TMPPY%"
echo c["language"] = "%LANG_CODE%" >> "%TMPPY%"
echo save_config^(c^) >> "%TMPPY%"
echo print^("  Config saved: language = %LANG_CODE%"^) >> "%TMPPY%"

if not exist "%TMPPY%" (
    echo [!] Failed to write temporary Python script: %TMPPY%
) else (
    "%PYTHON_CMD%" "%TMPPY%"
    if %errorlevel% neq 0 (
        echo [!] Failed to save config.
    )
    del "%TMPPY%" 2>nul
)
echo.

echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo   Default language: %LANG_CODE%
echo   Type 'check-cli' to start.
echo.
pause
exit /b 0

:uninstall
echo.
echo ========================================
echo   Uninstalling...
echo ========================================
echo.

set "PYTHON_CMD="

REM 优先使用 py launcher
where py >nul 2>&1 && set "PYTHON_CMD=py"

REM 尝试 python 命令
if not defined PYTHON_CMD where python >nul 2>&1 && set "PYTHON_CMD=python"

REM 尝试 python3 命令
if not defined PYTHON_CMD where python3 >nul 2>&1 && set "PYTHON_CMD=python3"

REM 尝试本地 venv
if not defined PYTHON_CMD if exist ".venv\Scripts\python.exe" set "PYTHON_CMD=%~dp0.venv\Scripts\python.exe"

REM 尝试 Microsoft Store Python 路径
if not defined PYTHON_CMD (
    for /f "tokens=*" %%i in ('dir /b "%LOCALAPPDATA%\Packages\*Python*" 2^>nul') do (
        for /f "tokens=*" %%j in ('dir /b "%LOCALAPPDATA%\Packages\%%i\LocalCache\Local\Python*" 2^>nul') do (
            if exist "%LOCALAPPDATA%\Packages\%%i\LocalCache\Local\%%j\python.exe" (
                set "PYTHON_CMD=%LOCALAPPDATA%\Packages\%%i\LocalCache\Local\%%j\python.exe"
            )
        )
    )
)

if not defined PYTHON_CMD (
    echo [!] Python not found. Cannot uninstall automatically.
    echo [!] Please run: pip uninstall multiformat-validator
    pause
    exit /b 1
)

echo [1/3] Uninstalling package...
%PYTHON_CMD% -m pip uninstall multiformat-validator -y
if %errorlevel% neq 0 (
    echo [!] Uninstall may have failed or package is not present.
) else (
    echo [v] Package uninstalled.
)
echo.

echo [2/3] Cleaning up config files...
if exist "%USERPROFILE%\.multiformat_validator\preferences.json" del "%USERPROFILE%\.multiformat_validator\preferences.json"
if exist "%USERPROFILE%\.multiformat_validator\.validator_history" del "%USERPROFILE%\.multiformat_validator\.validator_history"
if exist "%USERPROFILE%\.multiformat_validator\.validation_history.json" del "%USERPROFILE%\.multiformat_validator\.validation_history.json"
echo [v] Config files removed (if present).

echo.
echo [3/3] Cleaning user data directory...
set "USER_DATA=%USERPROFILE%\.multiformat_validator"
if exist "%USER_DATA%" (
    echo [!] Found user data at: %USER_DATA%
    if "%AUTO_NOPROMPT%"=="1" (
        rmdir /s /q "%USER_DATA%"
        echo [v] User data directory removed.
    ) else (
        set /p "CLEAN_USER=  Remove user data (settings, backups, rules)? (Y/N): "
        if /I "%CLEAN_USER%"=="Y" (
            rmdir /s /q "%USER_DATA%"
            echo [v] User data directory removed.
        ) else (
            echo [-] User data preserved.
        )
    )
) else (
    echo [v] No user data directory found.
)
echo.

echo ========================================
echo   Uninstall Complete!
echo ========================================
echo.
pause
exit /b 0

