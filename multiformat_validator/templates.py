import json
from pathlib import Path


TEMPLATES_DIR = Path.home() / ".multiformat_validator" / "templates"


def _ensure_dir():
    TEMPLATES_DIR.mkdir(exist_ok=True)


def save_template(name: str, config: dict) -> None:
    _ensure_dir()
    path = TEMPLATES_DIR / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def load_template(name: str) -> dict | None:
    path = TEMPLATES_DIR / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def delete_template(name: str) -> bool:
    path = TEMPLATES_DIR / f"{name}.json"
    if path.exists():
        path.unlink()
        return True
    return False


def list_templates() -> list[str]:
    _ensure_dir()
    return [f.stem for f in TEMPLATES_DIR.glob("*.json")]
