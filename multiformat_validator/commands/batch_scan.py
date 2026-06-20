from colorama import Fore, Style
from pathlib import Path
from ..display import clear_screen, show_progress_bar, display_batch_results
from ..exporter import export_json, export_csv, export_txt
from ..report import generate_comparison_report
from ..ui.prompts import clean_path


def run(i18n, output_format="text", output_file=None, config=None):
    from ..config import add_recent_folder
    from .validate import _log_result

    clear_screen()
    print(f"\n  {i18n.get('enter_folder')}\n")
    raw_path = input("  > ")
    folder_path = clean_path(raw_path)

    from . import _scan_folder
    show_progress_bar(i18n)
    results = _scan_folder(folder_path, config=config)

    if config:
        for r in results:
            _log_result(r["file"], r, config)
        add_recent_folder(folder_path)

    display_batch_results(i18n, results)

    if output_file:
        if output_format == "json":
            path = export_json(results, output_file)
        elif output_format == "csv":
            path = export_csv(results, output_file, i18n)
        elif output_format == "txt":
            path = export_txt(results, output_file, i18n)
        else:
            path = None
        if path:
            print(f"\n  {Fore.GREEN}{i18n.get('exported_to', path=path)}{Style.RESET_ALL}")
    else:
        export_choice = input(f"\n  {i18n.get('batch_export_format')}").strip().upper()
        if export_choice in ("JSON", "CSV", "TXT", "HTML"):
            print(f"\n  {i18n.get('enter_output_path')}")
            raw_output = input("  > ").strip()
            if raw_output:
                output_path = clean_path(raw_output)
            else:
                ext = {"JSON": "json", "CSV": "csv", "TXT": "txt", "HTML": "html"}[export_choice]
                output_path = str(Path.cwd() / f"batch_report.{ext}")

            if export_choice == "JSON":
                path = export_json(results, output_path)
            elif export_choice == "CSV":
                path = export_csv(results, output_path, i18n)
            elif export_choice == "TXT":
                path = export_txt(results, output_path, i18n)
            elif export_choice == "HTML":
                path = generate_comparison_report(results, i18n, str(Path(output_path).parent), filename=Path(output_path).name)
            print(f"  {Fore.GREEN}{i18n.get('saved_to', path=path)}{Style.RESET_ALL}")

    input(f"\n  {i18n.get('press_enter')}")
