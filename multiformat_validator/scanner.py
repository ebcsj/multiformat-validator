import os
import fnmatch
from pathlib import Path
from .validators import VALIDATORS
from .config import load_config
from .encoder import read_with_detection
from .file_validation import validate_content
from .plugins import get_plugin_validators

PROTECTED_PATHS = {
    "/etc", "/sys", "/proc", "/dev", "/boot",
    "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)",
}


def _is_excluded(path: Path, exclude_patterns: list[str]) -> bool:
    path_parts = path.parts
    for pattern in exclude_patterns:
        if not pattern:
            continue
        if pattern in path_parts:
            return True
        if any(fnmatch.fnmatch(part, pattern) for part in path_parts):
            return True
    return False


def _is_protected_path(path: Path) -> bool:
    resolved = path.resolve()
    for protected in PROTECTED_PATHS:
        try:
            if str(resolved).lower().startswith(protected.lower()):
                return True
        except (ValueError, OSError):
            continue
    return False


def _scan_files_stream(folder_path: Path, exclude_patterns: list[str], supported_extensions: set[str], max_bytes: int, recursive: bool = True):
    """流式生成文件路径，避免符号链接循环"""
    visited_real_paths = set()
    walk_results = os.walk(folder_path)
    if not recursive:
        walk_results = [(root, dirs, files) for root, dirs, files in walk_results if root == str(folder_path)]

    for root, dirs, files in walk_results:
        real_root = os.path.realpath(root)
        if real_root in visited_real_paths:
            continue
        visited_real_paths.add(real_root)

        dirs[:] = [d for d in dirs if not _is_excluded(Path(root) / d, exclude_patterns)]

        for file in files:
            filepath = Path(root) / file
            if _is_excluded(filepath, exclude_patterns):
                continue

            ext = filepath.suffix.lower()
            if ext not in supported_extensions:
                continue

            try:
                file_size = filepath.stat().st_size
                if file_size > max_bytes:
                    yield filepath, "OVERSIZE"
                    continue
            except OSError:
                continue

            yield filepath, "READY"


def scan_folder(folder_path: str, recursive: bool = True) -> list[dict]:
    results = []
    folder = Path(folder_path)

    try:
        folder = folder.resolve()
    except (ValueError, OSError):
        return [{"file": folder_path, "valid": False, "errors": [{"type": "InvalidPath", "line": 0, "col": 0, "message": f"Invalid path: {folder_path}", "fix": "Provide a valid path."}]}]

    config = load_config()
    exclude_patterns = config.get("exclude_patterns", [])
    max_size_mb = config.get("max_file_size_mb", 10)
    max_bytes = max_size_mb * 1024 * 1024
    ignore_errors = config.get("ignore_errors", [])
    supported_extensions = set(VALIDATORS.keys()) | set(get_plugin_validators().keys())

    if not folder.exists():
        return [{"file": folder_path, "valid": False, "errors": [{"type": "FolderNotFound", "line": 0, "col": 0, "message": f"Folder not found: {folder_path}", "fix": "Check the folder path."}]}]

    if not folder.is_dir():
        return [{"file": folder_path, "valid": False, "errors": [{"type": "NotADirectory", "line": 0, "col": 0, "message": f"Not a directory: {folder_path}", "fix": "Provide a valid directory path."}]}]

    if _is_protected_path(folder):
        return [{"file": folder_path, "valid": False, "errors": [{"type": "ProtectedPath", "line": 0, "col": 0, "message": f"Protected system directory: {folder_path}", "fix": "Scan a non-system directory."}]}]

    for filepath, status in _scan_files_stream(folder, exclude_patterns, supported_extensions, max_bytes, recursive):
        if status == "OVERSIZE":
            results.append({
                "file": str(filepath),
                "valid": False,
                "errors": [{"type": "FileTooLarge", "line": 0, "col": 0, "message": f"File exceeds max size ({max_size_mb} MB)", "fix": "Adjust max_file_size_mb in your preferences."}]
            })
            continue

        try:
            content, encoding = read_with_detection(str(filepath))
            if not content:
                results.append({"file": str(filepath), "valid": False, "errors": [{"type": "EmptyFile", "line": 0, "col": 0, "message": "File is empty or unreadable", "fix": "Check file content and permissions."}], "encoding": encoding})
                continue
            result = validate_content(str(filepath), content, ignore_errors)
            if result is None:
                continue
            results.append({"file": str(filepath), "valid": result.get("valid", False), "errors": result.get("errors", []), "encoding": encoding})
        except PermissionError:
            results.append({"file": str(filepath), "valid": False, "errors": [{"type": "PermissionError", "line": 0, "col": 0, "message": "Permission denied", "fix": "Check file permissions."}]})
        except FileNotFoundError:
            results.append({"file": str(filepath), "valid": False, "errors": [{"type": "FileNotFound", "line": 0, "col": 0, "message": "File not found", "fix": "Check file path."}]})
        except OSError as e:
            results.append({"file": str(filepath), "valid": False, "errors": [{"type": "OSError", "line": 0, "col": 0, "message": str(e), "fix": "Check file accessibility."}]})
        except Exception as e:
            results.append({"file": str(filepath), "valid": False, "errors": [{"type": "ReadError", "line": 0, "col": 0, "message": str(e), "fix": "Check file permissions and format."}]})

    return results
