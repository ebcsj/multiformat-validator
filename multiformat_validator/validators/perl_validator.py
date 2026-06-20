from .common import ValidationError, make_result


def validate_perl(content: str) -> dict:
    errors: list[ValidationError] = []
    lines = content.split("\n")
    brace_stack: list[tuple[int, int]] = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue

        for j, ch in enumerate(stripped):
            if ch == "{":
                brace_stack.append((i, j + 1))
            elif ch == "}":
                if brace_stack:
                    brace_stack.pop()
                else:
                    errors.append(ValidationError(
                        type="PerlUnmatchedBrace", line=i, col=j + 1,
                        message="Unexpected '}'",
                        fix="Check for missing '{'.",
                    ))

    for line_num, col in brace_stack:
        errors.append(ValidationError(
            type="PerlUnclosedBrace", line=line_num, col=col,
            message="Unclosed '{'",
            fix="Add '}' to close.",
        ))

    return make_result(errors)
