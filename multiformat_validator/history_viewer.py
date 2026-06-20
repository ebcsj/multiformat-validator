import json
import threading
import datetime
from pathlib import Path


HISTORY_FILE = Path.home() / ".multiformat_validator" / ".validation_history.json"
_history_lock = threading.Lock()


def _load() -> list[dict]:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def _save(data: list[dict]) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def add_record(file_path: str, valid: bool, error_count: int) -> None:
    with _history_lock:
        data = _load()
        data.insert(0, {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file": file_path,
            "valid": valid,
            "errors": error_count,
        })
        data = data[:100]
        _save(data)


def get_records() -> list[dict]:
    with _history_lock:
        return _load()


def clear_records() -> None:
    with _history_lock:
        _save([])


def export_records(output_path: str) -> str:
    with _history_lock:
        data = _load()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)
