import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from colorama import Fore, Style
from ..validators import VALIDATORS
from ..display import show_progress_bar, display_report
from ..history import save_last_path
from ..history_viewer import add_record
from ..report import generate_html_report
from ..exporter import export_json, export_csv, export_txt
from ..fixer import try_fix, apply_fixes, show_diff_preview
from ..encoder import read_with_detection
from ..ui.prompts import clean_path

def run(i18n, file_path, output_format="text", output_file=None, config=None):
    """执行单文件验证"""
    ignore = config.get("ignore_errors", []) if config else []
    show_progress_bar(i18n)
    result = _validate_file(file_path, ignore)
    save_last_path(file_path)
    add_record(file_path, result["valid"], len(result["errors"]))
    display_report(i18n, result, file_path)
    
    if config:
        _log_result(file_path, result, config)
        from multiformat_validator.config import add_recent_file
        add_recent_file(file_path)

    if output_file:
        _export_results(results=[{"file": file_path, "valid": result["valid"], "errors": result["errors"]}],
                       output_format=output_format, output_file=output_file, i18n=i18n)

    if not result["valid"]:
        _handle_fixes(file_path, result, i18n, ignore)

    input(f"\n  {i18n.get('press_enter')}")

def _validate_file(file_path: str, ignore_errors: list[str] | None = None) -> dict:
    """验证单个文件"""
    normalized = os.path.realpath(os.path.abspath(file_path))
    path = Path(normalized)
    
    if not path.exists():
        return {"valid": False, "errors": [{"type": "FileNotFound", "line": 0, "col": 0, 
                "message": f"File not found: {file_path}", "fix": "Check the file path and try again."}]}
    
    if not path.is_file():
        return {"valid": False, "errors": [{"type": "NotAFile", "line": 0, "col": 0, 
                "message": f"Not a file: {file_path}", "fix": "Provide a file path, not a directory."}]}
    
    ext = path.suffix.lower()

    try:
        content, encoding = read_with_detection(file_path)
    except (PermissionError, FileNotFoundError, OSError, Exception) as e:
        return {"valid": False, "errors": [{"type": type(e).__name__, "line": 0, "col": 0,
                "message": str(e), "fix": "Check file permissions and encoding."}]}

    if not content.strip():
        return {"valid": False, "errors": [{"type": "EmptyFile", "line": 0, "col": 0, 
                "message": f"File is empty: {file_path}", "fix": "File contains no content to validate."}]}

    errors_to_ignore = ignore_errors or []
    from ..file_validation import validate_content
    result = validate_content(file_path, content, errors_to_ignore)
    if result is None:
        return {"valid": False, "errors": [{"type": "UnsupportedFormat", "line": 0, "col": 0, 
                "message": f"Unsupported format: {ext}", "fix": f"Supported formats: {len(VALIDATORS)} types."}]}

    return result

def _log_result(file_path: str, result: dict, config: dict) -> None:
    """记录验证结果到日志"""
    if not config.get("logging_enabled"):
        return

    log_path = config.get("log_path", "validation.log")

    logger = logging.getLogger("ValidatorLogger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(
            log_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    status = "PASS" if result["valid"] else "FAIL"
    error_count = len(result["errors"])
    logger.info(f"{status} | {file_path} | Errors: {error_count}")

    for e in result["errors"]:
        logger.info(f"  - {e['type']}: {e['message']} (line {e['line']}, col {e['col']})")

def _export_results(results: list, output_format: str, output_file: str, i18n) -> None:
    """导出验证结果"""
    if output_format == "json":
        path = export_json(results, output_file)
        print(f"  {Fore.GREEN}{i18n.get('exported_to', path=path)}{Style.RESET_ALL}")
    elif output_format == "csv":
        path = export_csv(results, output_file, i18n)
        print(f"  {Fore.GREEN}{i18n.get('exported_to', path=path)}{Style.RESET_ALL}")
    elif output_format == "txt":
        path = export_txt(results, output_file, i18n)
        print(f"  {Fore.GREEN}{i18n.get('exported_to', path=path)}{Style.RESET_ALL}")

def _handle_fixes(file_path: str, result: dict, i18n, ignore: list) -> None:
    """处理自动修复"""
    fix_result = try_fix(file_path, result)
    if fix_result["fixes"]:
        print(f"\n  {Fore.YELLOW}{i18n.get('fixes_found', count=len(fix_result['fixes']))}{Style.RESET_ALL}")
        for fix in fix_result["fixes"][:5]:
            print(f"    {i18n.get('line_label', line=fix['line'])} {fix['type']} - {fix['message']}")
        
        if fix_result.get("fixed_content"):
            original_content, _ = read_with_detection(file_path)
            show_diff_preview(file_path, original_content, fix_result["fixed_content"], i18n)
        
        fix_choice = input(f"  {i18n.get('apply_fixes')}").strip().upper()
        if fix_choice == "Y":
            apply_fixes(file_path, fix_result["fixed_content"], fix_result.get("encoding"))
            print(f"  {Fore.GREEN}{i18n.get('fixes_applied', path=file_path)}{Style.RESET_ALL}")
            result = _validate_file(file_path, ignore)
            display_report(i18n, result, file_path)

    choice = input(f"\n  {i18n.get('export_html')}").strip().upper()
    if choice == "Y":
        print(f"\n  {i18n.get('enter_output_path')}")
        raw_output = input("  > ").strip()
        if raw_output:
            output_path = clean_path(raw_output)
            output_dir = str(Path(output_path).parent)
            report_path = generate_html_report(result, file_path, i18n, output_dir=output_dir, filename=Path(output_path).name)
        else:
            report_path = generate_html_report(result, file_path, i18n)
        print(f"  {Fore.GREEN}{i18n.get('report_saved', path=report_path)}{Style.RESET_ALL}")
