import re

from .common import ValidationError, make_result


def validate_markdown(content: str) -> dict:
    errors: list[ValidationError] = []
    lines = content.split("\n")
    link_pattern = re.compile(r"(!?\[)([^\]]*)(\])(\()([^)]*)(\))")

    for i, line in enumerate(lines, 1):
        hash_match = re.match(r"^(#{1,6})\s*(.*)", line)
        if hash_match:
            hashes = hash_match.group(1)
            rest = hash_match.group(2)

            if not rest:
                errors.append(ValidationError(
                    type="MDEmptyHeading", line=i, col=1,
                    message="Heading marker with no text",
                    fix="Add text after the '#' heading markers.",
                ))
            elif not line[len(hashes)].isspace() and line[len(hashes)] != "#":
                errors.append(ValidationError(
                    type="MDMissingSpaceAfterHash", line=i, col=len(hashes) + 1,
                    message=f"Heading marker '{hashes}' must be followed by a space",
                    fix=f"Add a space after '{hashes}', e.g. '{hashes} {rest}'",
                ))

        for match in link_pattern.finditer(line):
            bracket_content = match.group(2)
            paren_content = match.group(5)

            if not bracket_content and match.group(1) == "[":
                errors.append(ValidationError(
                    type="MDEmptyLinkText", line=i, col=match.start() + 1,
                    message="Empty link text in '[]'",
                    fix="Add text inside the square brackets.",
                ))

            if not paren_content:
                errors.append(ValidationError(
                    type="MDEmptyLinkUrl", line=i,
                    col=match.start() + len(match.group(1)) + len(match.group(2)) + len(match.group(3)) + 1,
                    message="Empty URL in link parentheses '()' ",
                    fix="Add a URL inside the parentheses.",
                ))

        j = 0
        while j < len(line):
            if line[j] == "[":
                bracket_depth = 1
                start_col = j + 1
                j += 1
                while j < len(line) and bracket_depth > 0:
                    if line[j] == "[":
                        bracket_depth += 1
                    elif line[j] == "]":
                        bracket_depth -= 1
                    j += 1

                if bracket_depth > 0:
                    errors.append(ValidationError(
                        type="MDUnclosedBracket", line=i, col=start_col,
                        message="Unclosed bracket '['",
                        fix="Add ']' to close the link text.",
                    ))
                else:
                    if j < len(line) and line[j] == "(":
                        paren_start = j + 1
                        j += 1
                        paren_depth = 1
                        while j < len(line) and paren_depth > 0:
                            if line[j] == "(":
                                paren_depth += 1
                            elif line[j] == ")":
                                paren_depth -= 1
                            j += 1

                        if paren_depth > 0:
                            errors.append(ValidationError(
                                type="MDUnclosedParen", line=i, col=paren_start,
                                message="Unclosed parenthesis '(' in link URL",
                                fix="Add ')' to close the link URL.",
                            ))
            else:
                j += 1

    return make_result(errors)
