import re

from .common import ValidationError, make_result

VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def validate_html(content: str) -> dict:
    errors: list[ValidationError] = []
    stack: list[tuple[str, int, int]] = []
    tag_pattern = re.compile(r"<(/?)(\w+)([^>]*)>")
    line_num = 1

    for line in content.split("\n"):
        for match in tag_pattern.finditer(line):
            is_closing = match.group(1) == "/"
            tag_name = match.group(2).lower()

            if tag_name in VOID_ELEMENTS:
                continue

            if is_closing:
                if not stack:
                    errors.append(ValidationError(
                        type="HTMLUnexpectedClose", line=line_num, col=match.start() + 1,
                        message=f"Unexpected closing tag </{tag_name}>",
                        fix=f"Remove </{tag_name}> or add corresponding opening tag.",
                    ))
                elif stack[-1][0] != tag_name:
                    errors.append(ValidationError(
                        type="HTMLMismatchedTag", line=line_num, col=match.start() + 1,
                        message=f"Tag mismatch: expected </{stack[-1][0]}> but found </{tag_name}>",
                        fix=f"Change </{tag_name}> to </{stack[-1][0]}> or fix the opening tag.",
                    ))
                    stack.pop()
                else:
                    stack.pop()
            else:
                if not match.group(3).rstrip().endswith("/"):
                    stack.append((tag_name, line_num, match.start() + 1))

        line_num += 1

    for tag_name, line, col in stack:
        errors.append(ValidationError(
            type="HTMLUnclosedTag", line=line, col=col,
            message=f"Unclosed tag <{tag_name}>",
            fix=f"Add </{tag_name}> to close the tag.",
        ))

    return make_result(errors)
