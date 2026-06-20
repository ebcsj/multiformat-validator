import ast
import sys

from .common import ValidationError, make_result


def validate_python(content: str) -> dict:
    errors: list[ValidationError] = []
    try:
        ast.parse(content)
    except SyntaxError as e:
        line = e.lineno or 0
        col = e.offset or 0
        current_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
        message = f"{e.msg}"
        fix = f"Check Python syntax at line {line}."
        
        if "future feature" in str(e.msg).lower() or "invalid syntax" in str(e.msg).lower():
            fix += f" [Note: Validator runs on Python {current_ver}. If file uses newer syntax, it may be falsely reported as error.]"
        
        errors.append(ValidationError(
            type="PythonSyntaxError", line=line, col=col,
            message=message, fix=fix,
        ))
    except Exception as e:
        errors.append(ValidationError(
            type="PythonSyntaxError", line=0, col=0,
            message=str(e), fix="Check Python file encoding and syntax.",
        ))
    return make_result(errors)
