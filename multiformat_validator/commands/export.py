from colorama import Fore, Style
from ..display import clear_screen, show_progress_bar
from ..exporter import export_json, export_csv, export_txt
from ..report import generate_comparison_report
from ..ui.prompts import clean_path


def run(i18n, config=None):
    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('batch_export_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    print(f"  {i18n.get('enter_folder')}")
    folder_path = clean_path(input("  > "))
    print(f"\n  {i18n.get('batch_export_format')}")
    fmt = input("  > ").strip().upper()
    if fmt not in ("JSON", "CSV", "TXT", "HTML"):
        fmt = "JSON"
    print(f"\n  {i18n.get('batch_export_output')}")
    output_name = input("  > ").strip()
    if not output_name:
        output_name = f"batch_report.{fmt.lower()}"

    from . import _scan_folder
    show_progress_bar(i18n)
    results = _scan_folder(folder_path, config=config)

    if fmt == "JSON":
        path = export_json(results, output_name)
    elif fmt == "CSV":
        path = export_csv(results, output_name, i18n)
    elif fmt == "TXT":
        path = export_txt(results, output_name, i18n)
    elif fmt == "HTML":
        path = generate_comparison_report(results, i18n, folder_path, filename=Path(output_name).name)
        output_name = path

    print(f"\n  {Fore.GREEN}{i18n.get('batch_export_saved', path=path)}{Style.RESET_ALL}")
    input(f"\n  {i18n.get('press_enter')}")
