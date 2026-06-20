import json
import shutil
import datetime
from pathlib import Path


_USER_DATA_DIR = Path.home() / ".multiformat_validator"
CONFIG_DIR = _USER_DATA_DIR
CONFIG_FILE = CONFIG_DIR / "preferences.json"
BACKUP_DIR = CONFIG_DIR / "backups"

DEFAULT_CONFIG = {
    "language": "en",
    "output_format": "text",
    "theme": "dark",
    "auto_export": False,
    "export_format": "json",
    "exclude_patterns": ["node_modules", ".git", "__pycache__", ".venv"],
    "max_file_size_mb": 10,
    "ignore_errors": [],
    "plugins": [],
    "logging_enabled": False,
    "log_path": "validation.log",
    "parallel_scanning": False,
    "parallel_workers": 4,
    "recent_files": [],
    "recent_folders": [],
    "window_width": 80,
    "window_height": 24,
    "confirm_exit": True,
    "show_startup_info": True,
    "last_language_menu": "en",
    "last_output_format": "text",
    "auto_check_updates": True,
    "history_max_records": 100,
    "export_template_default": None,
    "custom_validators_dir": None,
}


_config_cache = None


def _ensure_dirs():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def validate_config(config: dict) -> dict:
    sanitized = config.copy()

    valid_langs = {"zh_TW", "zh_CN", "en", "ja", "ko"}
    if sanitized.get("language") not in valid_langs:
        sanitized["language"] = "en"

    try:
        size = int(sanitized.get("max_file_size_mb", 10))
        sanitized["max_file_size_mb"] = size if size > 0 else 10
    except (ValueError, TypeError):
        sanitized["max_file_size_mb"] = 10

    try:
        workers = int(sanitized.get("parallel_workers", 4))
        sanitized["parallel_workers"] = max(1, min(workers, 32))
    except (ValueError, TypeError):
        sanitized["parallel_workers"] = 4

    try:
        max_records = int(sanitized.get("history_max_records", 100))
        sanitized["history_max_records"] = max(10, min(max_records, 1000))
    except (ValueError, TypeError):
        sanitized["history_max_records"] = 100

    return sanitized


def load_config() -> dict:
    global _config_cache
    if _config_cache is not None:
        return _config_cache.copy()

    _ensure_dirs()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                user_config = json.load(f)
            config = DEFAULT_CONFIG.copy()
            config.update(user_config)
            _config_cache = validate_config(config)
            return _config_cache.copy()
        except (json.JSONDecodeError, Exception):
            try:
                save_config(DEFAULT_CONFIG)
            except Exception:
                pass
            _config_cache = DEFAULT_CONFIG.copy()
            return _config_cache.copy()
    _config_cache = DEFAULT_CONFIG.copy()
    return _config_cache.copy()


def save_config(config: dict) -> None:
    global _config_cache
    _ensure_dirs()
    CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    _config_cache = config.copy()


def reset_config() -> dict:
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()


def backup_config() -> str | None:
    if not CONFIG_FILE.exists():
        return None
    _ensure_dirs()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"config_backup_{timestamp}.json"
    shutil.copy2(CONFIG_FILE, backup_path)
    return str(backup_path)


def restore_config(backup_name: str) -> bool:
    backup_path = BACKUP_DIR / backup_name
    if backup_path.exists():
        try:
            with open(backup_path, encoding="utf-8") as f:
                restored = json.load(f)
            config = DEFAULT_CONFIG.copy()
            config.update(restored)
            save_config(validate_config(config))
            return True
        except Exception:
            return False
    return False


def list_backups() -> list[str]:
    _ensure_dirs()
    return sorted([f.name for f in BACKUP_DIR.glob("config_backup_*.json")], reverse=True)


def export_config(output_path: str) -> str:
    config = load_config()
    path = Path(output_path)
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)


def import_config(input_path: str) -> dict | None:
    path = Path(input_path)
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                imported = json.load(f)
            config = DEFAULT_CONFIG.copy()
            config.update(imported)
            validated = validate_config(config)
            save_config(validated)
            return validated
        except Exception:
            return None
    return None


def add_recent_file(file_path: str) -> None:
    config = load_config()
    recent = config.get("recent_files", [])
    if file_path in recent:
        recent.remove(file_path)
    recent.insert(0, file_path)
    config["recent_files"] = recent[:20]
    save_config(config)


def add_recent_folder(folder_path: str) -> None:
    config = load_config()
    recent = config.get("recent_folders", [])
    if folder_path in recent:
        recent.remove(folder_path)
    recent.insert(0, folder_path)
    config["recent_folders"] = recent[:20]
    save_config(config)


def get_recent_files() -> list[str]:
    return load_config().get("recent_files", [])


def get_recent_folders() -> list[str]:
    return load_config().get("recent_folders", [])


def clear_recent() -> None:
    config = load_config()
    config["recent_files"] = []
    config["recent_folders"] = []
    save_config(config)


def get_config_path() -> str:
    return str(CONFIG_FILE)


def init_config() -> None:
    _ensure_dirs()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
