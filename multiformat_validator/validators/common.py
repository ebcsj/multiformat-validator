from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValidationError:
    type: str
    line: int
    col: int
    message: str
    fix: str

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "line": self.line,
            "col": self.col,
            "message": self.message,
            "fix": self.fix,
        }


EMPTY_ERRORS = []

def make_result(errors: list[ValidationError]) -> dict:
    if not errors:
        return {"valid": True, "errors": EMPTY_ERRORS}
    return {
        "valid": False,
        "errors": [e.to_dict() for e in errors]
    }


def check_brackets(
    lines: list[str],
    prefix: str,
    comment_prefixes: tuple[str, ...] = ("//", "/*"),
    skip_star: bool = True,
    check_parens: bool = True,
    check_braces: bool = True,
    check_brackets: bool = True,
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    paren_stack: list[tuple[int, int]] = []
    brace_stack: list[tuple[int, int]] = []
    bracket_stack: list[tuple[int, int]] = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if any(stripped.startswith(p) for p in comment_prefixes):
            continue
        if skip_star and stripped.startswith("*"):
            continue

        j = 0
        while j < len(stripped):
            ch = stripped[j]
            if ch in ('"', "'"):
                quote = ch
                j += 1
                while j < len(stripped):
                    if stripped[j] == "\\":
                        j += 2
                        continue
                    if stripped[j] == quote:
                        j += 1
                        break
                    j += 1
                continue
            if ch == "(" and check_parens:
                paren_stack.append((i, j + 1))
            elif ch == ")" and check_parens:
                if paren_stack:
                    paren_stack.pop()
                else:
                    errors.append(ValidationError(
                        type=f"{prefix}UnmatchedParen", line=i, col=j + 1,
                        message="Unexpected closing parenthesis ')'",
                        fix="Check for missing opening parenthesis '('.",
                    ))
            elif ch == "{" and check_braces:
                brace_stack.append((i, j + 1))
            elif ch == "}" and check_braces:
                if brace_stack:
                    brace_stack.pop()
                else:
                    errors.append(ValidationError(
                        type=f"{prefix}UnmatchedBrace", line=i, col=j + 1,
                        message="Unexpected closing brace '}'",
                        fix="Check for missing opening brace '{'.",
                    ))
            elif ch == "[" and check_brackets:
                bracket_stack.append((i, j + 1))
            elif ch == "]" and check_brackets:
                if bracket_stack:
                    bracket_stack.pop()
                else:
                    errors.append(ValidationError(
                        type=f"{prefix}UnmatchedBracket", line=i, col=j + 1,
                        message="Unexpected closing bracket ']'",
                        fix="Check for missing opening bracket '['.",
                    ))
            j += 1

    for line_num, col in paren_stack:
        errors.append(ValidationError(
            type=f"{prefix}UnclosedParen", line=line_num, col=col,
            message="Unclosed parenthesis '('",
            fix="Add ')' to close the expression.",
        ))
    for line_num, col in brace_stack:
        errors.append(ValidationError(
            type=f"{prefix}UnclosedBrace", line=line_num, col=col,
            message="Unclosed brace '{'",
            fix="Add '}' to close the block.",
        ))
    for line_num, col in bracket_stack:
        errors.append(ValidationError(
            type=f"{prefix}UnclosedBracket", line=line_num, col=col,
            message="Unclosed bracket '['",
            fix="Add ']' to close the array.",
        ))

    return errors
