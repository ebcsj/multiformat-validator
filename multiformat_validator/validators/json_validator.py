import json

from .common import ValidationError, make_result


def validate_json(content: str) -> dict:
    errors: list[ValidationError] = []
    try:
        json.loads(content)
    except json.JSONDecodeError as e:
        errors.append(ValidationError(
            type="JSONSyntaxError", line=e.lineno, col=e.colno,
            message=str(e.msg),
            fix="Check syntax around the reported position for missing commas, brackets, or quotes.",
        ))
    return make_result(errors)
