import re

from .common import ValidationError, make_result


def validate_bat(content: str) -> dict:
    errors: list[ValidationError] = []
    lines = content.split("\n")

    if not re.search(r"@?\s*echo\s+off", lines[0] if lines else "", re.IGNORECASE):
        errors.append(ValidationError(
            type="BATMissingEchoOff", line=1, col=1,
            message="Missing '@echo off' at the beginning of batch file",
            fix="Add '@echo off' as the first line to suppress command echoing.",
        ))

    paren_stack: list[int] = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.lower().startswith("rem"):
            continue

        for ch in stripped:
            if ch == "(":
                paren_stack.append(i)
            elif ch == ")":
                if paren_stack:
                    paren_stack.pop()
                else:
                    errors.append(ValidationError(
                        type="BATUnmatchedCloseParen", line=i, col=stripped.rfind(")") + 1,
                        message="Unmatched closing parenthesis",
                        fix="Check parenthesis balance in this line.",
                    ))

    for line_num in paren_stack:
        errors.append(ValidationError(
            type="BATUnclosedParen", line=line_num, col=1,
            message="Unclosed parenthesis block",
            fix="Add closing ')' for the open parenthesis block.",
        ))

    return make_result(errors)
