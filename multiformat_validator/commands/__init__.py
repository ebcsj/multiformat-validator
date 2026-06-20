from pathlib import Path
from colorama import Fore, Style
from .validate import run as run_validate
from .batch_scan import run as run_batch_scan
from .compare import run as run_compare
from .export import run as run_export
from ..scanner import scan_folder
from ..parallel_scanner import scan_folder_parallel
from ..exporter import export_json, export_csv, export_txt
from ..report import generate_comparison_report

__all__ = ['run_validate', 'run_batch_scan', 'run_compare', 'run_export', 'route_command']


def _scan_folder(folder_path, config=None, recursive=True):
    from ..config import load_config
    config = config or load_config()
    if config.get("parallel_scanning"):
        workers = config.get("parallel_workers", 4)
        return scan_folder_parallel(folder_path, recursive=recursive, max_workers=workers)
    return scan_folder(folder_path, recursive=recursive)


def route_command(args):
    from ..config import load_config
    from ..i18n import I18n

    config = load_config()
    lang = args.lang if args.lang != "en" else config.get("language", "en")
    i18n = I18n(lang)

    path = Path(args.path)
    if path.is_file():
        run_validate(i18n, str(path), args.format, args.output, config)
    elif path.is_dir():
        results = _scan_folder(str(path), config=config, recursive=args.recursive)
        if args.output:
            if args.format == "json":
                export_json(results, args.output)
            elif args.format == "csv":
                export_csv(results, args.output, i18n)
            elif args.format == "txt":
                export_txt(results, args.output, i18n)
            elif args.format == "html":
                html_path = generate_comparison_report(results, i18n, str(path), filename=Path(args.output).name)
                print(f"{i18n.get('cli_exported', path=html_path)}")
            print(f"{i18n.get('cli_exported', path=args.output)}")
        else:
            valid = sum(1 for r in results if r["valid"])
            print(i18n.get('cli_stats_summary', total=len(results), valid=valid, invalid=len(results) - valid))
    else:
        print(f"{Fore.RED}{i18n.get('cli_path_not_found', path=args.path)}{Style.RESET_ALL}")
