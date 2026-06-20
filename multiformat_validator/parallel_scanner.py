import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from .validators import VALIDATORS
from .encoder import read_with_detection
from .config import load_config
from .file_validation import validate_content
from .plugins import get_plugin_validators
from .scanner import _is_excluded, _is_protected_path


def scan_folder_parallel(folder_path: str, recursive: bool = True, max_workers: int = 4) -> list[dict]:
    config = load_config()
    exclude_patterns = config.get("exclude_patterns", [])
    max_size_mb = config.get("max_file_size_mb", 10)
    max_bytes = max_size_mb * 1024 * 1024
    ignore_errors = config.get("ignore_errors", [])
    supported_extensions = set(VALIDATORS.keys()) | set(get_plugin_validators().keys())

    folder = Path(folder_path)

    try:
        folder = folder.resolve()
    except (ValueError, OSError):
        return [{"file": folder_path, "valid": False, "errors": [{"type": "InvalidPath", "line": 0, "col": 0, "message": f"Invalid path: {folder_path}", "fix": "Provide a valid path."}]}]

    if not folder.exists():
        return [{"file": folder_path, "valid": False, "errors": [{"type": "FolderNotFound", "line": 0, "col": 0, "message": f"Folder not found: {folder_path}", "fix": "Check the folder path."}]}]

    if not folder.is_dir():
        return [{"file": folder_path, "valid": False, "errors": [{"type": "NotADirectory", "line": 0, "col": 0, "message": f"Not a directory: {folder_path}", "fix": "Provide a valid directory path."}]}]

    if _is_protected_path(folder):
        return [{"file": folder_path, "valid": False, "errors": [{"type": "ProtectedPath", "line": 0, "col": 0, "message": f"Protected system directory: {folder_path}", "fix": "Scan a non-system directory."}]}]

    visited_real_paths = set()
    files = []
    for root, dirs, files_list in os.walk(folder):
        real_root = os.path.realpath(root)
        if real_root in visited_real_paths:
            continue
        visited_real_paths.add(real_root)

        dirs[:] = [d for d in dirs if not _is_excluded(Path(root) / d, exclude_patterns)]

        for file in files_list:
            filepath = Path(root) / file
            if _is_excluded(filepath, exclude_patterns):
                continue
            ext = filepath.suffix.lower()
            if ext not in supported_extensions:
                continue
            try:
                file_size = filepath.stat().st_size
                if file_size > max_bytes:
                    files.append((filepath, "OVERSIZE"))
                    continue
            except OSError:
                continue
            files.append((filepath, "READY"))

        if not recursive:
            break

    def process_file(item):
        filepath, status = item
        if status == "OVERSIZE":
            return {"file": str(filepath), "valid": False, "errors": [{"type": "FileTooLarge", "line": 0, "col": 0, "message": f"File exceeds max size ({max_size_mb} MB)", "fix": "Adjust max_file_size_mb in your preferences."}]}

        try:
            content, encoding = read_with_detection(str(filepath))
            if not content:
                return {"file": str(filepath), "valid": False, "errors": [{"type": "EmptyFile", "line": 0, "col": 0, "message": "File is empty or unreadable", "fix": "Check file content and permissions."}], "encoding": encoding}
            result = validate_content(str(filepath), content, ignore_errors)
            if result is None:
                return None
            return {"file": str(filepath), "valid": result.get("valid", False), "errors": result.get("errors", []), "encoding": encoding}
        except PermissionError:
            return {"file": str(filepath), "valid": False, "errors": [{"type": "PermissionError", "line": 0, "col": 0, "message": "Permission denied", "fix": "Check file permissions."}]}
        except FileNotFoundError:
            return {"file": str(filepath), "valid": False, "errors": [{"type": "FileNotFound", "line": 0, "col": 0, "message": "File not found", "fix": "Check file path."}]}
        except OSError as e:
            return {"file": str(filepath), "valid": False, "errors": [{"type": "OSError", "line": 0, "col": 0, "message": str(e), "fix": "Check file accessibility."}]}
        except Exception as e:
            return {"file": str(filepath), "valid": False, "errors": [{"type": "ReadError", "line": 0, "col": 0, "message": str(e), "fix": "Check file permissions and format."}]}

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, item): item for item in files}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    return sorted(results, key=lambda x: x["file"])
