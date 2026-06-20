from colorama import Fore, Style
from ..display import clear_screen, show_progress_bar
from .validate import _validate_file
from ..ui.prompts import clean_path

def run(i18n, config=None):
    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('compare_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    print(f"  {i18n.get('enter_first_file')}")
    file_a = clean_path(input("  > "))
    print(f"\n  {i18n.get('enter_second_file')}")
    file_b = clean_path(input("  > "))

    ignore = config.get("ignore_errors", []) if config else []
    show_progress_bar(i18n)
    result_a = _validate_file(file_a, ignore)
    result_b = _validate_file(file_b, ignore)

    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('compare_result')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    errors_a = set(e["type"] for e in result_a["errors"])
    errors_b = set(e["type"] for e in result_b["errors"])

    print(f"  {Fore.WHITE}{i18n.get('compare_file_a')}: {file_a}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}{i18n.get('compare_file_b')}: {file_b}{Style.RESET_ALL}\n")

    if errors_a == errors_b and result_a["valid"] == result_b["valid"]:
        print(f"  {Fore.GREEN}{i18n.get('compare_same')}{Style.RESET_ALL}")
    else:
        print(f"  {Fore.YELLOW}{i18n.get('compare_diff')}{Style.RESET_ALL}\n")
        print(f"  {Fore.RED}{i18n.get('compare_errors_a')}: {len(result_a['errors'])}{Style.RESET_ALL}")
        for e in result_a["errors"]:
            print(f"    - {e['type']}: {e['message']}")
        print(f"\n  {Fore.RED}{i18n.get('compare_errors_b')}: {len(result_b['errors'])}{Style.RESET_ALL}")
        for e in result_b["errors"]:
            print(f"    - {e['type']}: {e['message']}")

    input(f"\n  {i18n.get('press_enter')}")
