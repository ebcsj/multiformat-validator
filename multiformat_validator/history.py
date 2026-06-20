import threading
from pathlib import Path


HISTORY_FILE = Path.home() / ".multiformat_validator" / ".validator_history"
_history_lock = threading.Lock()


def get_last_path() -> str | None:
    with _history_lock:
        if HISTORY_FILE.exists():
            try:
                content = HISTORY_FILE.read_text(encoding="utf-8").strip()
                if content:
                    return content
            except Exception:
                pass
    return None


def save_last_path(file_path: str) -> None:
    with _history_lock:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(file_path, encoding="utf-8")


def clear_history() -> None:
    with _history_lock:
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
