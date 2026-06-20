import json
import re
from pathlib import Path

MAX_LINE_LENGTH = 1000

RULES_DIR = Path.home() / ".multiformat_validator" / "rules"


def _ensure_dir():
    RULES_DIR.mkdir(parents=True, exist_ok=True)


def load_rules() -> list[dict]:
    _ensure_dir()
    rules = []
    for f in RULES_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if _validate_rule(data):
                data["_source"] = str(f)
                rules.append(data)
        except Exception:
            pass
    return rules


def save_rule(name: str, rule: dict) -> str:
    _ensure_dir()
    path = RULES_DIR / f"{name}.json"
    path.write_text(json.dumps(rule, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)


def delete_rule(name: str) -> bool:
    path = RULES_DIR / f"{name}.json"
    if path.exists():
        path.unlink()
        return True
    return False


def list_rules() -> list[dict]:
    return load_rules()


def _validate_rule(rule: dict) -> bool:
    required = ["name", "pattern", "file_patterns"]
    return all(k in rule for k in required)


def _matches_file(file_path: str, file_patterns: list[str]) -> bool:
    from pathlib import Path
    ext = Path(file_path).suffix.lower()
    for pattern in file_patterns:
        pattern = pattern.strip().lower()
        if pattern.startswith("*."):
            if ext == pattern[1:]:
                return True
        elif ext == pattern:
            return True
    return False


def check_custom_rules(file_path: str, content: str) -> list[dict]:
    rules = load_rules()
    errors = []

    for rule in rules:
        if not _matches_file(file_path, rule.get("file_patterns", [])):
            continue

        try:
            pattern = re.compile(rule["pattern"])
        except re.error:
            continue

        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            check_line = line[:MAX_LINE_LENGTH]
            for match in pattern.finditer(check_line):
                errors.append({
                    "type": f"CustomRule:{rule['name']}",
                    "line": i,
                    "col": match.start() + 1,
                    "message": rule.get("message", f"Rule '{rule['name']}' triggered"),
                    "fix": rule.get("fix", "Check the custom rule."),
                    "severity": rule.get("severity", "warning"),
                    "rule_name": rule["name"],
                })

    return errors
