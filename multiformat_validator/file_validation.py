"""Shared file validation logic for single-file and batch scanning."""

from pathlib import Path

from .validators import VALIDATORS
from .rules_engine import check_custom_rules
from .plugins import get_plugin_validators


def validate_content(
    file_path: str,
    content: str,
    ignore_errors: list[str] | None = None,
) -> dict | None:
    """Validate file content. Returns None if the extension is not supported."""
    path = Path(file_path)
    if path.name == "__init__.py" and not content.strip():
        return {"valid": True, "errors": []}

    if not content.strip():
        return {
            "valid": False,
            "errors": [{
                "type": "EmptyFile",
                "line": 0,
                "col": 0,
                "message": f"File is empty: {file_path}",
                "fix": "File contains no content to validate.",
            }],
        }

    ext = Path(file_path).suffix.lower()
    result = None

    if ext in VALIDATORS:
        result = VALIDATORS[ext](content)
    else:
        plugin_validators = get_plugin_validators()
        if ext in plugin_validators:
            try:
                result = plugin_validators[ext](content)
            except Exception as e:
                result = {
                    "valid": False,
                    "errors": [{
                        "type": "PluginError",
                        "line": 0,
                        "col": 0,
                        "message": str(e),
                        "fix": "Check plugin code.",
                    }],
                }

    if result is None:
        return None

    custom_errors = check_custom_rules(file_path, content)
    if custom_errors:
        result["errors"].extend(custom_errors)
        result["valid"] = len(result["errors"]) == 0

    if ignore_errors:
        ignore_set = set(ignore_errors)
        result["errors"] = [e for e in result["errors"] if e["type"] not in ignore_set]
        result["valid"] = len(result["errors"]) == 0

    return result
