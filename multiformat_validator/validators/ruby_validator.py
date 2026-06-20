import re

from .common import ValidationError, make_result


def validate_ruby(content: str) -> dict:
    errors: list[ValidationError] = []
    lines = content.split("\n")
    end_stack: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue

        if re.match(r"^\s*(def|class|module|if|unless|while|until|for|begin|case)\b", stripped):
            if not stripped.endswith("do") and not stripped.endswith("|") and ":" not in stripped.split("#")[0]:
                end_stack.append((i, "end"))

        if re.match(r"^\s*do\s*(\|.*\|)?\s*$", stripped) or re.match(r"^\s*do\s+\|", stripped):
            end_stack.append((i, "end"))

        if re.match(r"^\s*end\s*$", stripped):
            if end_stack:
                end_stack.pop()
            else:
                errors.append(ValidationError(
                    type="RubyUnmatchedEnd", line=i, col=1,
                    message="Unexpected 'end'",
                    fix="Check for missing opening block.",
                ))

    for line_num, _block_type in end_stack:
        errors.append(ValidationError(
            type="RubyUnclosedBlock", line=line_num, col=1,
            message="Unclosed block (missing 'end')",
            fix="Add 'end' to close the block.",
        ))

    return make_result(errors)
