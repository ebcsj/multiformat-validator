import re

from .common import ValidationError, make_result


def validate_lua(content: str) -> dict:
    errors: list[ValidationError] = []
    lines = content.split("\n")
    block_stack: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("--"):
            continue

        if re.match(r"^\s*(function|if|for|while|repeat|do)\b", stripped):
            block_stack.append((i, "block"))

        if re.match(r"^\s*end\s*$", stripped) or re.match(r"^\s*end\s*[,;)]", stripped):
            if block_stack:
                block_stack.pop()
            else:
                errors.append(ValidationError(
                    type="LuaUnmatchedEnd", line=i, col=1,
                    message="Unexpected 'end'",
                    fix="Check for missing opening block.",
                ))

        if re.match(r"^\s*until\b", stripped):
            if block_stack:
                block_stack.pop()
            else:
                errors.append(ValidationError(
                    type="LuaUnmatchedUntil", line=i, col=1,
                    message="Unexpected 'until'",
                    fix="Check for missing 'repeat'.",
                ))

    for line_num, _block_type in block_stack:
        errors.append(ValidationError(
            type="LuaUnclosedBlock", line=line_num, col=1,
            message="Unclosed block (missing 'end')",
            fix="Add 'end' to close the block.",
        ))

    return make_result(errors)
