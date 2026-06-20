import ast
import json
from pathlib import Path


CUSTOM_DIR = Path.home() / ".multiformat_validator" / "custom_validators"

FORBIDDEN_NAMES = {
    "__import__", "compile", "exec", "eval", "open", "breakpoint",
    "exit", "quit", "copyright", "credits", "license", "help",
    "input", "globals", "locals", "vars", "dir", "getattr", "setattr",
    "delattr", "hasattr", "type", "super", "memoryview", "staticmethod",
    "classmethod", "property",
}

SAFE_BUILTINS = {
    "print": print,
    "len": len,
    "range": range,
    "enumerate": enumerate,
    "zip": zip,
    "map": map,
    "filter": filter,
    "sorted": sorted,
    "reversed": reversed,
    "min": min,
    "max": max,
    "sum": sum,
    "abs": abs,
    "round": round,
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
    "tuple": tuple,
    "set": set,
    "frozenset": frozenset,
    "True": True,
    "False": False,
    "None": None,
}


def _check_code_safety(code: str) -> str | None:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Syntax error: {e}"

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
            return f"Forbidden name: {node.id}"
        if isinstance(node, ast.Import):
            return "Import statements are not allowed"
        if isinstance(node, ast.ImportFrom):
            return "Import statements are not allowed"
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id in ("os", "sys", "shutil", "subprocess", "pathlib", "socket", "urllib", "requests"):
                return f"Access to {node.value.id} module is not allowed"
    return None


def _ensure_dir():
    CUSTOM_DIR.mkdir(exist_ok=True)


def save_validator(name: str, pattern: str, code: str) -> None:
    _ensure_dir()
    path = CUSTOM_DIR / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "name": name,
        "pattern": pattern,
        "code": code,
    }, indent=2, ensure_ascii=False), encoding="utf-8")


def load_validator(name: str) -> dict | None:
    path = CUSTOM_DIR / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def delete_validator(name: str) -> bool:
    path = CUSTOM_DIR / f"{name}.json"
    if path.exists():
        path.unlink()
        return True
    return False


def list_validators() -> list[dict]:
    _ensure_dir()
    validators = []
    for f in CUSTOM_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            validators.append(data)
        except Exception:
            pass
    return validators


def run_validator(name: str, content: str) -> dict:
    v = load_validator(name)
    if not v:
        return {"valid": False, "errors": [{"type": "NotFound", "line": 0, "col": 0, "message": f"Validator '{name}' not found", "fix": "Create the validator first."}]}

    code = v["code"]
    safety_error = _check_code_safety(code)
    if safety_error:
        return {"valid": False, "errors": [{"type": "SecurityError", "line": 0, "col": 0, "message": f"Code rejected: {safety_error}", "fix": "Remove forbidden operations from your validator code."}]}

    try:
        local_vars = {"content": content, "errors": []}
        safe_globals = {"__builtins__": SAFE_BUILTINS}
        exec(code, safe_globals, local_vars)
        return {"valid": len(local_vars.get("errors", [])) == 0, "errors": local_vars.get("errors", [])}
    except Exception as e:
        return {"valid": False, "errors": [{"type": "PluginError", "line": 0, "col": 0, "message": str(e), "fix": "Check your validator code."}]}
