import re

from .common import ValidationError, make_result


def validate_ini(content: str) -> dict:
    errors: list[ValidationError] = []
    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        if not stripped or stripped.startswith((";", "#")):
            continue

        if stripped.startswith("["):
            if not stripped.endswith("]"):
                errors.append(ValidationError(
                    type="INIUnclosedSection", line=i, col=len(stripped),
                    message=f"Unclosed section header: '{stripped}'",
                    fix="Add ']' to close the section header.",
                ))
                continue

            section_content = stripped[1:-1].strip()
            if not section_content:
                errors.append(ValidationError(
                    type="INIEmptySection", line=i, col=2,
                    message="Empty section header '[]'",
                    fix="Add a section name inside the brackets.",
                ))
            continue

        if "=" in stripped:
            if not re.match(r"^([a-zA-Z0-9_.]+)\s*=\s*(.*)$", stripped):
                errors.append(ValidationError(
                    type="INIInvalidKey", line=i, col=1,
                    message=f"Invalid key format: '{stripped.split('=')[0].strip()}'",
                    fix="Key must contain only letters, numbers, underscores, or dots.",
                ))
        else:
            errors.append(ValidationError(
                type="INIInvalidFormat", line=i, col=1,
                message=f"Invalid INI format: '{stripped}'",
                fix="Use 'key = value' format or '[Section]' for sections.",
            ))

    return make_result(errors)
