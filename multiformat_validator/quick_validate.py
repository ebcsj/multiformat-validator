import sys
import subprocess
import ctypes
import os
import shutil
from pathlib import Path


SCRIPT_PATH = Path.home() / ".multiformat_validator" / "quick_validate.bat"
REG_KEY = r"HKCU\Software\Classes\*\shell\CheckCLI"


def is_admin() -> bool:
    if os.name != "nt":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        return False


def _find_python_for_script() -> str:
    """找到适合在 batch 脚本中使用的 Python 路径"""
    # 优先使用 py launcher（最可靠）
    py_exe = shutil.which("py")
    if py_exe:
        return "py"
    
    # 尝试 python
    python_exe = shutil.which("python")
    if python_exe:
        # 检查是否是 Microsoft Store Python（WindowsApps 路径）
        if "WindowsApps" in python_exe:
            return "python"  # 使用命令而不是完整路径
        return python_exe
    
    # 回退到 sys.executable
    return sys.executable


def _create_script() -> str:
    python_exe = _find_python_for_script()
    script = f'''@echo off
"{python_exe}" -m multiformat_validator "%~1"
pause
'''
    SCRIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCRIPT_PATH.write_text(script, encoding="utf-8")
    return str(SCRIPT_PATH)


def _registry_key_exists() -> bool:
    if os.name != "nt":
        return False
    try:
        result = subprocess.run(
            f'reg query "{REG_KEY}"',
            shell=True, capture_output=True, text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def install_context_menu(i18n=None) -> tuple[bool, str]:
    def _t(key, **kw):
        return i18n.get(key, **kw) if i18n else key

    if os.name != "nt":
        return False, _t("quick_only_windows")

    try:
        script_path = _create_script()
        reg_commands = [
            f'reg add "{REG_KEY}" /ve /t REG_SZ /d "Validate with CheckCLI" /f',
            f'reg add "{REG_KEY}\\command" /ve /t REG_SZ /d "\\"{script_path}\\" \\"%1\\"" /f',
        ]
        for cmd in reg_commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                if "Access is denied" in result.stderr or "拒绝访问" in result.stderr:
                    return False, _t("quick_access_denied")
                return False, _t("quick_registry_error", error=result.stderr)
        return True, _t("quick_installed")
    except Exception as e:
        return False, _t("quick_install_failed", error=str(e))


def uninstall_context_menu(i18n=None) -> tuple[bool, str]:
    def _t(key, **kw):
        return i18n.get(key, **kw) if i18n else key

    if os.name != "nt":
        return False, _t("quick_only_windows")

    try:
        if _registry_key_exists():
            result = subprocess.run(
                f'reg delete "{REG_KEY}" /f',
                shell=True, capture_output=True, text=True
            )
            if result.returncode != 0:
                if "Access is denied" in result.stderr or "拒绝访问" in result.stderr:
                    return False, _t("quick_access_denied")
                return False, _t("quick_registry_error", error=result.stderr)

        if SCRIPT_PATH.exists():
            SCRIPT_PATH.unlink()

        return True, _t("quick_uninstalled")
    except Exception as e:
        return False, _t("quick_uninstall_failed", error=str(e))
