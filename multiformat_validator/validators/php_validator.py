import re

from .common import ValidationError, make_result


def validate_php(content: str) -> dict:
    errors: list[ValidationError] = []
    lines = content.split("\n")

    has_php_tag = any(re.search(r"<\?php", line) for line in lines[:3])
    if not has_php_tag:
        errors.append(ValidationError(
            type="PHPMissingOpeningTag", line=1, col=1,
            message="PHP file must contain '<?php' in the first 3 lines",
            fix="Add '<?php' at the beginning of the file.",
        ))

    brace_stack: list[tuple[int, int]] = []
    control_pattern = re.compile(
        r"^\s*(if|elseif|else|for|foreach|while|switch|do|function|class|interface|trait|namespace|use)\b"
    )

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        if not stripped or stripped.startswith(("//", "#", "/*", "*")):
            continue

        for j, ch in enumerate(stripped):
            if ch == "{":
                brace_stack.append((i, j + 1))
            elif ch == "}":
                if brace_stack:
                    brace_stack.pop()
                else:
                    errors.append(ValidationError(
                        type="PHPUnmatchedBrace", line=i, col=j + 1,
                        message="Unexpected closing brace '}'",
                        fix="Check for missing opening brace '{'.",
                    ))

        if stripped.endswith(("{", "}", ",")):
            continue
        if control_pattern.match(stripped):
            continue

        if re.match(r"^[a-zA-Z_]\w*\s*=", stripped):
            var_name = stripped.split("=")[0].strip()
            if not var_name.startswith("$"):
                errors.append(ValidationError(
                    type="PHPVariableMustStartWithDollar", line=i, col=1,
                    message=f"Variable '{var_name}' must start with '$'",
                    fix=f"Change '{var_name}' to '${var_name}'.",
                ))
                continue

        if stripped.startswith("return") and not stripped.endswith(";"):
            errors.append(ValidationError(
                type="PHPMissingSemicolon", line=i, col=len(stripped),
                message="Statement missing semicolon",
                fix="Add ';' at the end of the statement.",
            ))
            continue

        if re.match(r"^\$\w+", stripped) and not stripped.endswith((";", "{", "}", ",", ")", "]")):
            errors.append(ValidationError(
                type="PHPMissingSemicolon", line=i, col=len(stripped),
                message="Variable declaration missing semicolon",
                fix="Add ';' at the end of the statement.",
            ))

    for line_num, col in brace_stack:
        errors.append(ValidationError(
            type="PHPUnclosedBrace", line=line_num, col=col,
            message="Unclosed brace '{'",
            fix="Add '}' to close the code block.",
        ))

    return make_result(errors)
