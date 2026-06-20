import hashlib
import importlib.util
import json
from pathlib import Path


PLUGINS_DIR = Path.home() / ".multiformat_validator" / "plugins"
PLUGIN_REGISTRY = PLUGINS_DIR / "registry.json"


def _ensure_dir():
    PLUGINS_DIR.mkdir(parents=True, exist_ok=True)


def _is_safe_path(plugin_path: str) -> bool:
    try:
        resolved = Path(plugin_path).resolve()
        plugins_resolved = PLUGINS_DIR.resolve()
        return str(resolved).startswith(str(plugins_resolved))
    except (ValueError, OSError):
        return False


def _file_hash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def copy_to_plugins_dir(source_path: str) -> Path | None:
    src = Path(source_path)
    if not src.exists() or not src.is_file():
        return None
    dest = PLUGINS_DIR / src.name
    dest.write_bytes(src.read_bytes())
    return dest


def _load_registry() -> list[dict]:
    _ensure_dir()
    if PLUGIN_REGISTRY.exists():
        try:
            return json.loads(PLUGIN_REGISTRY.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []


def _save_registry(plugins: list[dict]) -> None:
    _ensure_dir()
    PLUGIN_REGISTRY.write_text(
        json.dumps(plugins, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def register_plugin(plugin_path: str, confirm: bool = False) -> dict | None:
    path = Path(plugin_path)
    if not path.exists():
        return None

    if not _is_safe_path(plugin_path):
        return None

    try:
        spec = importlib.util.spec_from_file_location("_plugin_temp", str(path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        return None

    name = getattr(module, "PLUGIN_NAME", path.stem)
    extensions = getattr(module, "PLUGIN_EXTENSIONS", [])
    validate_func = getattr(module, "validate", None)

    if not validate_func or not callable(validate_func):
        return None

    plugin_info = {
        "name": name,
        "path": str(path.resolve()),
        "extensions": extensions,
        "hash": _file_hash(path),
    }

    registry = _load_registry()
    registry = [p for p in registry if p["name"] != name]
    registry.append(plugin_info)
    _save_registry(registry)

    return plugin_info


def unregister_plugin(name: str) -> bool:
    registry = _load_registry()
    new_registry = [p for p in registry if p["name"] != name]
    if len(new_registry) < len(registry):
        _save_registry(new_registry)
        return True
    return False


def list_plugins() -> list[dict]:
    return _load_registry()


def get_plugin_validators() -> dict[str, callable]:
    registry = _load_registry()
    validators = {}

    for plugin_info in registry:
        path = Path(plugin_info["path"])
        if not path.exists():
            continue

        expected_hash = plugin_info.get("hash")
        if expected_hash and _file_hash(path) != expected_hash:
            continue

        try:
            spec = importlib.util.spec_from_file_location(
                f"_plugin_{plugin_info['name']}", str(path)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            validate_func = getattr(module, "validate", None)
            if validate_func and callable(validate_func):
                for ext in plugin_info.get("extensions", []):
                    validators[ext] = validate_func
        except Exception:
            continue

    return validators
