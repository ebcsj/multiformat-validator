import shutil
import difflib
from pathlib import Path
from .encoder import read_with_detection
from colorama import Fore, Style


FIXABLE_ERRORS = {
    "PythonSyntaxError": "_fix_python_indent",
    "PythonIndentationError": "_fix_python_indent",
    "MDEmptyHeading": "_fix_md_empty_heading",
    "MDMissingSpaceAfterHash": "_fix_md_space_after_hash",
    "CSSMissingSemicolon": "_fix_css_semicolon",
    "PHPMissingSemicolon": "_fix_php_semicolon",
    "BATMissingEchoOff": "_fix_bat_echo_off",
    "INIUnclosedSection": "_fix_ini_section",
}


def _fix_python_indent(content: str, error: dict) -> str | None:
    lines = content.split("\n")
    line_idx = error["line"] - 1
    if line_idx < 0 or line_idx >= len(lines):
        return None
    line = lines[line_idx]
    stripped = line.lstrip()
    if stripped and not line.startswith("\t") and not line.startswith("    "):
        indent = len(line) - len(stripped)
        if indent > 0:
            return None
    if not stripped:
        return None
    if stripped.startswith(("def ", "class ", "if ", "for ", "while ")) and not stripped.endswith(":"):
        lines[line_idx] = line.rstrip() + ":"
        return "\n".join(lines)
    return None


def _fix_md_empty_heading(content: str, error: dict) -> str | None:
    lines = content.split("\n")
    line_idx = error["line"] - 1
    if line_idx < 0 or line_idx >= len(lines):
        return None
    lines[line_idx] = ""
    return "\n".join(lines)


def _fix_md_space_after_hash(content: str, error: dict) -> str | None:
    lines = content.split("\n")
    line_idx = error["line"] - 1
    if line_idx < 0 or line_idx >= len(lines):
        return None
    line = lines[line_idx]
    stripped = line.lstrip()
    hashes = ""
    for ch in stripped:
        if ch == "#":
            hashes += ch
        else:
            break
    rest = stripped[len(hashes):]
    if rest and not rest.startswith(" "):
        lines[line_idx] = line.replace(hashes + rest, hashes + " " + rest, 1)
        return "\n".join(lines)
    return None


def _fix_css_semicolon(content: str, error: dict) -> str | None:
    lines = content.split("\n")
    line_idx = error["line"] - 1
    if line_idx < 0 or line_idx >= len(lines):
        return None
    line = lines[line_idx].rstrip()
    if line and not line.endswith((";", "{", "}", ",")):
        lines[line_idx] = line + ";"
        return "\n".join(lines)
    return None


def _fix_php_semicolon(content: str, error: dict) -> str | None:
    lines = content.split("\n")
    line_idx = error["line"] - 1
    if line_idx < 0 or line_idx >= len(lines):
        return None
    line = lines[line_idx].rstrip()
    if line and not line.endswith((";", "{", "}", ",", ")", "]")):
        lines[line_idx] = line + ";"
        return "\n".join(lines)
    return None


def _fix_bat_echo_off(content: str, error: dict) -> str | None:
    lines = content.split("\n")
    if lines:
        lines.insert(0, "@echo off")
        return "\n".join(lines)
    return None


def _fix_ini_section(content: str, error: dict) -> str | None:
    lines = content.split("\n")
    line_idx = error["line"] - 1
    if line_idx < 0 or line_idx >= len(lines):
        return None
    line = lines[line_idx].rstrip()
    if line.startswith("[") and not line.endswith("]"):
        lines[line_idx] = line + "]"
        return "\n".join(lines)
    return None


FIX_FUNCTIONS = {
    "PythonSyntaxError": _fix_python_indent,
    "PythonIndentationError": _fix_python_indent,
    "MDEmptyHeading": _fix_md_empty_heading,
    "MDMissingSpaceAfterHash": _fix_md_space_after_hash,
    "CSSMissingSemicolon": _fix_css_semicolon,
    "PHPMissingSemicolon": _fix_php_semicolon,
    "BATMissingEchoOff": _fix_bat_echo_off,
    "INIUnclosedSection": _fix_ini_section,
}


def try_fix(file_path: str, result: dict) -> dict:
    # Read using encoding detection to avoid corrupting files with non-utf8 encodings
    content, encoding = read_with_detection(file_path)
    fixes_applied = []

    for error in result.get("errors", []):
        error_type = error.get("type", "")
        fix_func = FIX_FUNCTIONS.get(error_type)
        if not fix_func:
            continue
        fixed_content = fix_func(content, error)
        if fixed_content and fixed_content != content:
            fixes_applied.append({
                "line": error["line"],
                "type": error_type,
                "message": error["message"],
                "original": content.split("\n")[error["line"] - 1] if error["line"] > 0 else "",
                "fixed": fixed_content.split("\n")[error["line"] - 1] if error["line"] > 0 else "",
            })
            content = fixed_content

    return {
        "fixes": fixes_applied,
        "fixed_content": content if fixes_applied else None,
        "encoding": encoding if fixes_applied else None,
    }


def show_diff_preview(filepath: str, original_content: str, fixed_content: str, i18n=None) -> bool:
    orig_lines = original_content.splitlines(keepends=True)
    fixed_lines = fixed_content.splitlines(keepends=True)

    diff = difflib.unified_diff(
        orig_lines, fixed_lines,
        fromfile=f"a/{filepath} ({i18n.get('diff_original') if i18n else 'Original'})",
        tofile=f"b/{filepath} ({i18n.get('diff_fixed') if i18n else 'Auto-fixed'})"
    )

    has_changes = False
    print(f"\n{Fore.CYAN}=== {i18n.get('diff_preview_title') if i18n else 'Diff Preview'} ==={Style.RESET_ALL}")

    for line in diff:
        has_changes = True
        if line.startswith('+') and not line.startswith('+++'):
            print(f"{Fore.GREEN}{line.rstrip()}{Style.RESET_ALL}")
        elif line.startswith('-') and not line.startswith('---'):
            print(f"{Fore.RED}{line.rstrip()}{Style.RESET_ALL}")
        elif line.startswith('@@'):
            print(f"{Fore.BLUE}{line.rstrip()}{Style.RESET_ALL}")
        else:
            print(line.rstrip())

    if not has_changes:
        print(i18n.get('diff_no_changes') if i18n else "No changes needed. File is perfect!")
    print(f"{Fore.CYAN}==================================={Style.RESET_ALL}\n")
    return has_changes


def apply_fixes(file_path: str, fixed_content: str, encoding: str | None = None) -> None:
    backup_path = f"{file_path}.bak"
    try:
        shutil.copy2(file_path, backup_path)
    except Exception:
        pass
    enc = encoding or "utf-8"
    Path(file_path).write_text(fixed_content, encoding=enc)
