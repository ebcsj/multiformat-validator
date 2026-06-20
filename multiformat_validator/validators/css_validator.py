import re

from .common import ValidationError, make_result


def validate_css(content: str) -> dict:
    errors: list[ValidationError] = []
    brace_stack: list[tuple[int, int]] = []
    lines = content.split("\n")
    inside_brace = False
    in_block_comment = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        if in_block_comment:
            if "*/" in stripped:
                in_block_comment = False
            continue

        if not stripped or stripped.startswith("//"):
            continue

        if stripped.startswith("/*"):
            if "*/" not in stripped[2:]:
                in_block_comment = True
            continue

        for j, ch in enumerate(stripped):
            if ch == "{":
                brace_stack.append((i, j + 1))
                inside_brace = True
            elif ch == "}":
                if brace_stack:
                    brace_stack.pop()
                    if not brace_stack:
                        inside_brace = False
                else:
                    errors.append(ValidationError(
                        type="CSSUnmatchedBrace", line=i, col=j + 1,
                        message="Unexpected closing brace '}'",
                        fix="Check for missing opening brace '{'.",
                    ))

        if inside_brace and ":" in stripped:
            if not stripped.endswith(("{", "}", ";")):
                if not re.match(r"^[\s]*@", stripped):
                    errors.append(ValidationError(
                        type="CSSMissingSemicolon", line=i, col=len(stripped),
                        message="Missing semicolon at end of CSS property",
                        fix="Add ';' at the end of the CSS property.",
                    ))

    for line_num, col in brace_stack:
        errors.append(ValidationError(
            type="CSSUnclosedBrace", line=line_num, col=col,
            message="Unclosed brace '{'",
            fix="Add '}' to close the CSS rule block.",
        ))

    return make_result(errors)
