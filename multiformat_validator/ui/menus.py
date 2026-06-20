import sys
from colorama import Fore, Style
from .. import __version__
from ..validators import VALIDATORS
from ..history import get_last_path, clear_history
from ..history_viewer import get_records, clear_records, export_records
from ..display import clear_screen, show_progress_bar, display_batch_results
from ..stats import scan_folder_stats
from ..custom_validators import save_validator, delete_validator, list_validators
from ..quick_validate import install_context_menu, uninstall_context_menu
from ..rules_engine import save_rule, delete_rule, list_rules
from ..plugins import register_plugin, unregister_plugin, list_plugins, PLUGINS_DIR
from ..templates import save_template, load_template, delete_template, list_templates
from ..config import load_config, save_config
from ..colors import set_theme, c
from .prompts import clean_path


def _print_header(i18n, text):
    print(f"\n{c()['header']}{'=' * 50}{Style.RESET_ALL}")
    print(f"{c()['title']}  {text}{Style.RESET_ALL}")
    print(f"{c()['header']}{'=' * 50}{Style.RESET_ALL}\n")


def _print_line(label, value, color_key="success"):
    print(f"  {c()[color_key]}{label}:{Style.RESET_ALL} {value}")


def interactive_mode(i18n, config):
    set_theme(config.get("theme", "dark"))
    while True:
        clear_screen()
        last_path = get_last_path()

        _print_header(i18n, f"MultiFormat Validator CLI v{__version__}")

        if last_path:
            print(f"  {c()['header']}[0] {i18n.get('option_retry', path=last_path)}{Style.RESET_ALL}")
        print(f"  [1] {i18n.get('option_check_file')}")
        print(f"  [2] {i18n.get('option_batch_scan')}")
        print(f"  [3] {i18n.get('option_file_browser')}")
        print(f"  [4] {i18n.get('option_compare')}")
        print(f"  [5] {i18n.get('option_batch_export')}")
        print(f"  [6] {i18n.get('option_templates')}")
        print(f"  [7] {i18n.get('option_stats')}")
        print(f"  [8] {i18n.get('option_history')}")
        print(f"  [9] {i18n.get('option_custom_validators')}")
        print(f"  {c()['accent']}[R] {i18n.get('option_custom_rules')}{Style.RESET_ALL}")
        print(f"  {c()['accent']}[P] {i18n.get('option_plugins')}{Style.RESET_ALL}")
        print(f"  {c()['accent']}[Q] {i18n.get('option_quick_validate')}{Style.RESET_ALL}")
        print(f"  {c()['title']}[S] {i18n.get('option_settings')}{Style.RESET_ALL}")
        print(f"  {c()['accent']}[H] {i18n.get('option_help')}{Style.RESET_ALL}")
        print(f"  {c()['error']}[X] {i18n.get('option_exit')}{Style.RESET_ALL}\n")

        choice = input("  > ").strip().upper()

        if choice == "0" and last_path:
            clear_screen()
            from ..commands.validate import run as run_validation
            run_validation(i18n, last_path, config=config)
        elif choice == "1":
            clear_screen()
            from ..commands.validate import run as run_validation
            print(f"\n  {i18n.get('enter_path')}\n")
            raw_path = input("  > ")
            file_path = clean_path(raw_path)
            run_validation(i18n, file_path, config=config)
        elif choice == "2":
            from ..commands.batch_scan import run as run_batch_scan
            run_batch_scan(i18n, config=config)
        elif choice == "3":
            from ..browser import browse_folder
            from ..commands.validate import run as run_validation
            selected = browse_folder(i18n=i18n)
            if selected:
                run_validation(i18n, selected, config=config)
        elif choice == "4":
            from ..commands.compare import run as run_compare
            run_compare(i18n, config)
        elif choice == "5":
            from ..commands.export import run as run_export
            run_export(i18n, config)
        elif choice == "6":
            manage_templates(i18n, config)
        elif choice == "7":
            show_stats(i18n)
        elif choice == "8":
            show_history(i18n)
        elif choice == "9":
            manage_custom_validators(i18n)
        elif choice == "R":
            manage_rules(i18n)
        elif choice == "P":
            manage_plugins(i18n)
        elif choice == "Q":
            manage_quick_validate(i18n)
        elif choice == "S":
            i18n, config = settings_menu(i18n, config)
        elif choice == "H":
            show_help(i18n)
        elif choice == "X":
            clear_screen()
            print(f"\n  {i18n.get('goodbye')}\n")
            sys.exit(0)


def show_help(i18n):
    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('help_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    print(f"  {Fore.GREEN}{i18n.get('version')}:{Style.RESET_ALL} v{__version__}")
    print(f"  {Fore.GREEN}{i18n.get('formats')}:{Style.RESET_ALL} {i18n.get('help_extensions', count=len(VALIDATORS))}\n")

    print(f"  {Fore.YELLOW}{i18n.get('help_main_menu')}:{Style.RESET_ALL}")
    print(f"    {i18n.get('help_opt_0')}")
    print(f"    {i18n.get('help_opt_1')}")
    print(f"    {i18n.get('help_opt_2')}")
    print(f"    {i18n.get('help_opt_3')}")
    print(f"    {i18n.get('help_opt_4')}")
    print(f"    {i18n.get('help_opt_5')}\n")

    print(f"  {Fore.YELLOW}{i18n.get('help_cli_usage')}:{Style.RESET_ALL}")
    print(f"    {i18n.get('help_cli_start')}")
    print(f"    {i18n.get('help_cli_file')}")
    print(f"    {i18n.get('help_cli_scan')}")
    print(f"    {i18n.get('help_cli_lang')}")
    print(f"    {i18n.get('help_cli_export')}")
    print(f"    {i18n.get('help_cli_list')}")
    print(f"    {i18n.get('help_cli_ver')}\n")

    print(f"  {Fore.YELLOW}{i18n.get('help_languages')}:{Style.RESET_ALL}")
    print(f"    zh_TW 繁體中文 | zh_CN 简体中文 | en English")
    print(f"    ja 日本語 | ko 한국어\n")

    print(f"  {Fore.YELLOW}{i18n.get('help_formats')}:{Style.RESET_ALL}")
    print(f"    JSON, Python, HTML, XML, BAT/CMD, PHP, CSS, Markdown,")
    print(f"    INI, JavaScript, TypeScript, Java, C#, Go, Ruby, Rust,")
    print(f"    Kotlin, Swift, Perl, Lua, Scala, YAML, SQL\n")

    input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def settings_menu(i18n, config):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('settings_title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

        lang_names = {
            "zh_TW": "繁體中文", "zh_CN": "简体中文", "en": "English",
            "ja": "日本語", "ko": "한국어"
        }
        current_lang = lang_names.get(config.get("language", "en"), "English")
        current_theme = config.get("theme", "dark")
        current_fmt = config.get("output_format", "text")
        logging_status = i18n.get('log_enabled') if config.get("logging_enabled") else i18n.get('log_disabled')
        ignore_list = ", ".join(config.get("ignore_errors", [])) or i18n.get('rules_none')

        print(f"  [1] {i18n.get('change_language')}      ({i18n.get('current')}: {Fore.GREEN}{current_lang}{Style.RESET_ALL})")
        print(f"  [2] {i18n.get('change_output_format')}  ({i18n.get('current')}: {Fore.GREEN}{current_fmt}{Style.RESET_ALL})")
        print(f"  [3] {i18n.get('change_theme')}        ({i18n.get('current')}: {Fore.GREEN}{current_theme}{Style.RESET_ALL})")
        print(f"  [4] {i18n.get('clear_history')}")
        print(f"  [5] {i18n.get('rules_title')}       ({i18n.get('current')}: {Fore.GREEN}{ignore_list}{Style.RESET_ALL})")
        print(f"  [6] {i18n.get('plugins_title')}")
        print(f"  [7] {i18n.get('log_title')}          ({Fore.GREEN}{logging_status}{Style.RESET_ALL})")
        print(f"  [8] {i18n.get('check_updates')}")
        print(f"  [9] {i18n.get('version_info')}")
        print(f"  [C] {i18n.get('config_title')}")
        print(f"  [0] {i18n.get('back')}\n")

        choice = input("  > ").strip().upper()

        if choice == "0":
            return i18n, config
        elif choice == "1":
            i18n, config = change_language(config)
        elif choice == "2":
            config = change_output_format(config)
        elif choice == "3":
            config = change_theme(config)
        elif choice == "4":
            clear_history()
            print(f"\n  {Fore.GREEN}{i18n.get('history_cleared')}{Style.RESET_ALL}")
            input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "5":
            config = manage_ignore_errors(i18n, config)
        elif choice == "6":
            manage_plugins(i18n)
        elif choice == "7":
            config = toggle_logging(i18n, config)
        elif choice == "8":
            check_for_updates(i18n, config)
        elif choice == "9":
            show_version_info(i18n)
        elif choice == "C":
            config = manage_config(i18n, config)


def change_language(config):
    from ..i18n import I18n

    clear_screen()
    i18n = I18n(config.get("language", "en"))
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('change_language_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    lang_names = {
        "1": ("zh_TW", "繁體中文"), "2": ("zh_CN", "简体中文"), "3": ("en", "English"),
        "4": ("ja", "日本語"), "5": ("ko", "한국어")
    }

    for num, (code, name) in lang_names.items():
        marker = f"{Fore.GREEN} {i18n.get('current_marker')}" if config.get("language") == code else ""
        print(f"  {num}. {name}{marker}")

    print()
    choice = input("  > ").strip()

    if choice in lang_names:
        code, name = lang_names[choice]
        config["language"] = code
        save_config(config)
        i18n = I18n(code)
        print(f"\n  {Fore.GREEN}{i18n.get('language_changed', lang=name)}{Style.RESET_ALL}")
        input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        return i18n, config

    return I18n(config.get("language", "en")), config


def change_output_format(config):
    from ..i18n import I18n

    clear_screen()
    i18n = I18n(config.get("language", "en"))
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('change_format_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    formats = {"1": "text", "2": "json", "3": "csv"}
    for num, fmt in formats.items():
        marker = f"{Fore.GREEN} {i18n.get('current_marker')}" if config.get("output_format") == fmt else ""
        print(f"  {num}. {fmt}{marker}")

    print()
    choice = input("  > ").strip()

    if choice in formats:
        config["output_format"] = formats[choice]
        save_config(config)
        i18n = I18n(config.get("language", "en"))
        print(f"\n  {Fore.GREEN}{i18n.get('format_changed', format=formats[choice])}{Style.RESET_ALL}")
        input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")

    return config


def change_theme(config):
    from ..i18n import I18n

    clear_screen()
    i18n = I18n(config.get("language", "en"))
    _print_header(i18n, i18n.get('theme_title'))

    themes = {"1": "dark", "2": "light"}
    labels = {"1": i18n.get('theme_dark'), "2": i18n.get('theme_light')}

    for num, theme in themes.items():
        marker = f" {c()['success']}{i18n.get('current_marker')}{Style.RESET_ALL}" if config.get("theme") == theme else ""
        print(f"  {num}. {labels[num]}{marker}")

    print()
    choice = input("  > ").strip()

    if choice in themes:
        config["theme"] = themes[choice]
        save_config(config)
        set_theme(themes[choice])
        print(f"\n  {c()['success']}{i18n.get('theme_changed', theme=themes[choice])}{Style.RESET_ALL}")
        input(f"  {c()['info']}{i18n.get('press_enter')}{Style.RESET_ALL}")

    return config


def manage_ignore_errors(i18n, config):
    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('rules_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    current = config.get("ignore_errors", [])
    current_str = ", ".join(current) if current else i18n.get('rules_none')
    print(f"  {i18n.get('rules_current', rules=current_str)}\n")
    print(f"  {i18n.get('rules_ignore')}")
    raw = input("  > ").strip()

    if raw:
        config["ignore_errors"] = [e.strip() for e in raw.split(",") if e.strip()]
    else:
        config["ignore_errors"] = []

    save_config(config)
    print(f"\n  {Fore.GREEN}{i18n.get('rules_saved')}{Style.RESET_ALL}")
    input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
    return config


def toggle_logging(i18n, config):
    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('log_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    status = i18n.get('log_enabled') if config.get("logging_enabled") else i18n.get('log_disabled')
    print(f"  {i18n.get('log_path')}: {config.get('log_path', 'validation.log')}")
    print(f"  {status}\n")

    print(f"  [1] {i18n.get('log_enable')}")
    print(f"  [2] {i18n.get('log_disable')}")
    print(f"  [0] {i18n.get('back')}\n")

    choice = input("  > ").strip()

    if choice == "1":
        config["logging_enabled"] = True
        save_config(config)
        print(f"\n  {Fore.GREEN}{i18n.get('log_enabled')}{Style.RESET_ALL}")
    elif choice == "2":
        config["logging_enabled"] = False
        save_config(config)
        print(f"\n  {Fore.GREEN}{i18n.get('log_disabled')}{Style.RESET_ALL}")

    input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
    return config


def manage_config(i18n, config):
    from ..config import (
        reset_config, backup_config,
        restore_config, list_backups, export_config, import_config,
        get_recent_files, get_recent_folders, clear_recent, get_config_path
    )

    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('config_title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

        print(f"  {i18n.get('config_path')}: {get_config_path()}\n")
        print(f"  [1] {i18n.get('config_view')}")
        print(f"  [2] {i18n.get('config_export')}")
        print(f"  [3] {i18n.get('config_import')}")
        print(f"  [4] {i18n.get('config_backup')}")
        print(f"  [5] {i18n.get('config_restore')}")
        print(f"  [6] {i18n.get('config_backups')}")
        print(f"  [7] {i18n.get('config_reset')}")
        print(f"  [8] {i18n.get('config_recent_files')}")
        print(f"  [9] {i18n.get('config_recent_folders')}")
        print(f"  [C] {i18n.get('config_clear_recent')}")
        print(f"  [0] {i18n.get('back')}\n")

        choice = input("  > ").strip().upper()

        if choice == "0":
            return config
        elif choice == "1":
            clear_screen()
            print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  {i18n.get('config_current_values')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")
            for key, value in config.items():
                print(f"  {Fore.GREEN}{key}:{Style.RESET_ALL} {value}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "2":
            print(f"\n  {i18n.get('config_enter_path')}")
            path = input("  > ").strip()
            if path:
                exported = export_config(path)
                print(f"\n  {Fore.GREEN}{i18n.get('config_exported', path=exported)}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "3":
            print(f"\n  {i18n.get('config_enter_path')}")
            path = input("  > ").strip()
            if path:
                imported = import_config(path)
                if imported:
                    config = imported
                    print(f"\n  {Fore.GREEN}{i18n.get('config_imported')}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.RED}{i18n.get('config_import_failed')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "4":
            backup_path = backup_config()
            if backup_path:
                print(f"\n  {Fore.GREEN}{i18n.get('config_backed_up', path=backup_path)}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "5":
            backups = list_backups()
            if backups:
                print(f"\n  {i18n.get('config_available_backups')}")
                for b in backups:
                    print(f"    - {b}")
                print(f"\n  {i18n.get('config_enter_backup')}")
                name = input("  > ").strip()
                if restore_config(name):
                    config = load_config()
                    print(f"\n  {Fore.GREEN}{i18n.get('config_restored', name=name)}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.RED}{i18n.get('config_restore_failed')}{Style.RESET_ALL}")
            else:
                print(f"\n  {i18n.get('config_no_backups')}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "6":
            backups = list_backups()
            clear_screen()
            print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  {i18n.get('config_backups')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")
            if backups:
                for b in backups:
                    print(f"    - {b}")
            else:
                print(f"  {i18n.get('config_no_backups')}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "7":
            config = reset_config()
            print(f"\n  {Fore.GREEN}{i18n.get('config_reset_done')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "8":
            recent = get_recent_files()
            clear_screen()
            print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  {i18n.get('config_recent_files')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")
            if recent:
                for f in recent[:20]:
                    print(f"    - {f}")
            else:
                print(f"  {i18n.get('history_none')}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "9":
            recent = get_recent_folders()
            clear_screen()
            print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  {i18n.get('config_recent_folders')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")
            if recent:
                for f in recent[:20]:
                    print(f"    - {f}")
            else:
                print(f"  {i18n.get('history_none')}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "C":
            clear_recent()
            print(f"\n  {Fore.GREEN}{i18n.get('config_recent_cleared')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def check_for_updates(i18n, config=None):
    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('check_updates')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    print(f"  {Fore.WHITE}{i18n.get('version')}: v{__version__}{Style.RESET_ALL}\n")

    if config and not config.get("auto_check_updates", True):
        print(f"  {Fore.YELLOW}{i18n.get('update_disabled')}{Style.RESET_ALL}")
        input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        return

    try:
        import urllib.request
        import json
        url = "https://pypi.org/pypi/multiformat-validator/json"
        print(f"  {Fore.YELLOW}{i18n.get('checking_updates')}{Style.RESET_ALL}")
        req = urllib.request.Request(url, headers={"User-Agent": "check-cli"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            latest = data["info"]["version"]
            latest_parts = tuple(int(x) for x in latest.split(".")[:3])
            current_parts = tuple(int(x) for x in __version__.split(".")[:3])
            if latest_parts > current_parts:
                print(f"  {Fore.GREEN}{i18n.get('update_available', version=latest)}{Style.RESET_ALL}")
                print(f"  {Fore.WHITE}{i18n.get('update_command')}{Style.RESET_ALL}")
            else:
                print(f"  {Fore.GREEN}{i18n.get('up_to_date')}{Style.RESET_ALL}")
    except Exception:
        print(f"  {Fore.YELLOW}{i18n.get('could_not_check')}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}{i18n.get('visit_pypi')}{Style.RESET_ALL}")

    input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def show_version_info(i18n):
    from ..i18n import I18n

    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('version_info_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    print(f"  {Fore.GREEN}{i18n.get('name')}:{Style.RESET_ALL}    {i18n.get('app_name')}")
    print(f"  {Fore.GREEN}{i18n.get('version')}:{Style.RESET_ALL} v{__version__}")
    print(f"  {Fore.GREEN}Python:{Style.RESET_ALL}  {sys.version.split()[0]}")
    print(f"  {Fore.GREEN}{i18n.get('formats')}:{Style.RESET_ALL} {len(VALIDATORS)} extensions")
    print(f"  {Fore.GREEN}{i18n.get('languages')}:{Style.RESET_ALL} 5 (zh_TW, zh_CN, en, ja, ko)")
    print(f"  {Fore.GREEN}{i18n.get('author')}:{Style.RESET_ALL}   Kerby Chow\n")

    input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def manage_templates(i18n, config):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('templates_title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

        templates = list_templates()
        if templates:
            print(f"  {i18n.get('templates_list')}:")
            for t in templates:
                print(f"    - {t}")
        else:
            print(f"  {i18n.get('templates_none')}")

        print(f"\n  [1] {i18n.get('templates_save')}")
        print(f"  [2] {i18n.get('templates_load')}")
        print(f"  [3] {i18n.get('templates_delete')}")
        print(f"  [0] {i18n.get('back')}\n")

        choice = input("  > ").strip()

        if choice == "0":
            return config
        elif choice == "1":
            print(f"\n  {i18n.get('templates_enter_name')}")
            name = input("  > ").strip()
            if name:
                save_template(name, config)
                print(f"\n  {Fore.GREEN}{i18n.get('templates_saved', name=name)}{Style.RESET_ALL}")
                input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "2":
            if templates:
                print(f"\n  {i18n.get('template_enter_name')}")
                name = input("  > ").strip()
                loaded = load_template(name)
                if loaded:
                    config.update(loaded)
                    save_config(config)
                    print(f"\n  {Fore.GREEN}{i18n.get('templates_loaded', name=name)}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.RED}{i18n.get('template_not_found')}{Style.RESET_ALL}")
                input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "3":
            if templates:
                print(f"\n  {i18n.get('template_enter_delete')}")
                name = input("  > ").strip()
                if delete_template(name):
                    print(f"\n  {Fore.GREEN}{i18n.get('templates_deleted', name=name)}{Style.RESET_ALL}")
                input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def show_stats(i18n):
    from pathlib import Path

    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('stats_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    print(f"  {i18n.get('enter_folder')}")
    folder = clean_path(input("  > "))

    folder_path = Path(folder)
    if not folder_path.exists():
        print(f"\n  {Fore.RED}{i18n.get('error_directory_not_found', path=folder)}{Style.RESET_ALL}")
        input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        return
    if not folder_path.is_dir():
        print(f"\n  {Fore.RED}{i18n.get('error_not_a_file', path=folder)}{Style.RESET_ALL}")
        input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        return

    show_progress_bar(i18n)
    stats = scan_folder_stats(folder)

    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('stats_summary')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    print(f"  {Fore.GREEN}{i18n.get('stats_total_files')}:{Style.RESET_ALL} {stats['files']}")
    print(f"  {Fore.GREEN}{i18n.get('stats_total_lines')}:{Style.RESET_ALL} {stats['total']}")
    print(f"  {Fore.GREEN}{i18n.get('stats_code')}:{Style.RESET_ALL} {stats['code']}")
    print(f"  {Fore.GREEN}{i18n.get('stats_comments')}:{Style.RESET_ALL} {stats['comments']}")
    print(f"  {Fore.GREEN}{i18n.get('stats_blank')}:{Style.RESET_ALL} {stats['blank']}\n")

    if stats["languages"]:
        print(f"  {Fore.YELLOW}{i18n.get('stats_languages')}:{Style.RESET_ALL}")
        for ext, data in sorted(stats["languages"].items(), key=lambda x: -x[1]["lines"]):
            print(f"    {ext}: {i18n.get('stats_ext_summary', count=data['files'], lines=data['lines'])}")

    print(f"\n  [0] {i18n.get('back')}\n")
    input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def show_history(i18n):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('history_title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

        records = get_records()
        if records:
            print(f"  {Fore.WHITE}{i18n.get('history_recent')}:{Style.RESET_ALL}\n")
            for r in records[:10]:
                status = f"{Fore.GREEN}{i18n.get('history_pass')}" if r["valid"] else f"{Fore.RED}{i18n.get('history_fail')}"
                print(f"  {r['date']} | {status}{Style.RESET_ALL} | {r['file']} ({i18n.get('history_error_count', count=r['errors'])})")
        else:
            print(f"  {i18n.get('history_none')}")

        print(f"\n  [1] {i18n.get('history_export')}")
        print(f"  [2] {i18n.get('history_clear')}")
        print(f"  [0] {i18n.get('back')}\n")

        choice = input("  > ").strip()

        if choice == "0":
            return
        elif choice == "1":
            if records:
                print(f"\n  {i18n.get('enter_output_path')}")
                raw_output = input("  > ").strip()
                if raw_output:
                    output_path = clean_path(raw_output)
                else:
                    output_path = "validation_history.json"
                path = export_records(output_path)
                print(f"\n  {Fore.GREEN}{i18n.get('history_exported', path=path)}{Style.RESET_ALL}")
                input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "2":
            clear_records()
            print(f"\n  {Fore.GREEN}{i18n.get('history_cleared')}{Style.RESET_ALL}")
            input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def manage_custom_validators(i18n):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('custom_title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

        validators = list_validators()
        if validators:
            print(f"  {i18n.get('custom_list')}:")
            for v in validators:
                print(f"    - {v['name']} ({v['pattern']})")
        else:
            print(f"  {i18n.get('custom_none')}")

        print(f"\n  [1] {i18n.get('custom_create')}")
        print(f"  [2] {i18n.get('custom_delete')}")
        print(f"  [0] {i18n.get('back')}\n")

        choice = input("  > ").strip()

        if choice == "0":
            return
        elif choice == "1":
            print(f"\n  {i18n.get('custom_name')}")
            name = input("  > ").strip()
            print(f"  {i18n.get('custom_pattern')}")
            pattern = input("  > ").strip()
            print(f"  {i18n.get('custom_code')}")
            print(f"  {i18n.get('custom_enter_finish')}")
            code_lines = []
            while True:
                line = input()
                if line == "":
                    break
                code_lines.append(line)
            code = "\n".join(code_lines)
            if name and code:
                save_validator(name, pattern, code)
                print(f"\n  {Fore.GREEN}{i18n.get('custom_saved', name=name)}{Style.RESET_ALL}")
                input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "2":
            if validators:
                print(f"\n  {i18n.get('custom_enter_delete')}")
                name = input("  > ").strip()
                if delete_validator(name):
                    print(f"\n  {Fore.GREEN}{i18n.get('custom_deleted', name=name)}{Style.RESET_ALL}")
                input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def manage_quick_validate(i18n):
    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('quick_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    print(f"  {i18n.get('quick_info')}\n")
    print(f"  [1] {i18n.get('quick_install')}")
    print(f"  [2] {i18n.get('quick_uninstall')}")
    print(f"  [0] {i18n.get('back')}\n")

    choice = input("  > ").strip()

    if choice == "1":
        success, message = install_context_menu(i18n)
        if success:
            print(f"\n  {Fore.GREEN}{i18n.get('quick_installed')}{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.RED}{i18n.get('quick_failed_install')}{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}{message}{Style.RESET_ALL}")
    elif choice == "2":
        success, message = uninstall_context_menu(i18n)
        if success:
            print(f"\n  {Fore.GREEN}{i18n.get('quick_uninstalled')}{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.RED}{i18n.get('quick_failed_uninstall')}{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}{message}{Style.RESET_ALL}")

    input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def manage_rules(i18n):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('custom_rules_title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

        rules = list_rules()
        if rules:
            print(f"  {i18n.get('custom_rules_active')}")
            for r in rules:
                severity = r.get("severity", "warning")
                print(f"    - {r['name']} [{severity}] -> {r.get('file_patterns', [])}")
        else:
            print(f"  {i18n.get('custom_rules_none')}")

        print(f"\n  [1] {i18n.get('custom_rules_create')}")
        print(f"  [2] {i18n.get('custom_rules_delete')}")
        print(f"  [3] {i18n.get('custom_rules_view')}")
        print(f"  [0] {i18n.get('back')}\n")

        choice = input("  > ").strip()

        if choice == "0":
            return
        elif choice == "1":
            print(f"\n  {i18n.get('custom_rules_rule_name')}")
            name = input("  > ").strip()
            print(f"  {i18n.get('custom_rules_file_patterns')}")
            patterns = input("  > ").strip()
            print(f"  {i18n.get('custom_rules_regex')}")
            pattern = input("  > ").strip()
            print(f"  {i18n.get('custom_rules_severity')}")
            severity = input("  > ").strip() or "warning"
            print(f"  {i18n.get('custom_rules_error_msg')}")
            message = input("  > ").strip()
            print(f"  {i18n.get('custom_rules_fix_suggestion')}")
            fix = input("  > ").strip()

            if name and pattern and patterns:
                rule = {
                    "name": name,
                    "file_patterns": [p.strip() for p in patterns.split(",")],
                    "pattern": pattern,
                    "severity": severity,
                    "message": message,
                    "fix": fix,
                }
                save_rule(name, rule)
                print(f"\n  {Fore.GREEN}{i18n.get('custom_rules_created', name=name)}{Style.RESET_ALL}")
            else:
                print(f"\n  {Fore.RED}{i18n.get('custom_rules_required')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "2":
            if rules:
                print(f"\n  {i18n.get('custom_rules_enter_delete')}")
                name = input("  > ").strip()
                if delete_rule(name):
                    print(f"\n  {Fore.GREEN}{i18n.get('custom_rules_deleted', name=name)}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.RED}{i18n.get('custom_rules_not_found')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "3":
            if rules:
                print(f"\n  {i18n.get('custom_rules_enter_view')}")
                name = input("  > ").strip()
                for r in rules:
                    if r["name"] == name:
                        print(f"\n  {i18n.get('custom_rules_label_name', value=r['name'])}")
                        print(f"  {i18n.get('custom_rules_label_patterns', value=r.get('file_patterns', []))}")
                        print(f"  {i18n.get('custom_rules_label_regex', value=r.get('pattern', ''))}")
                        print(f"  {i18n.get('custom_rules_label_severity', value=r.get('severity', 'warning'))}")
                        print(f"  {i18n.get('custom_rules_label_message', value=r.get('message', ''))}")
                        print(f"  {i18n.get('custom_rules_label_fix', value=r.get('fix', ''))}")
                        break
                else:
                    print(f"\n  {Fore.RED}{i18n.get('custom_rules_not_found')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def manage_plugins(i18n):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('plugins_title_menu')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

        plugins = list_plugins()
        if plugins:
            print(f"  {i18n.get('plugins_loaded_list')}")
            for p in plugins:
                exts = ", ".join(p.get("extensions", []))
                print(f"    - {p['name']} ({exts})")
        else:
            print(f"  {i18n.get('plugins_none_loaded')}")

        print(f"\n  [1] {i18n.get('plugins_load_menu')}")
        print(f"  [2] {i18n.get('plugins_unload_menu')}")
        print(f"  [0] {i18n.get('back')}\n")

        choice = input("  > ").strip()

        if choice == "0":
            return
        elif choice == "1":
            print(f"\n  {i18n.get('plugins_enter_path')}")
            path = input("  > ").strip()
            path = clean_path(path)
            from ..plugins import _is_safe_path
            if not _is_safe_path(path):
                print(f"\n  {Fore.RED}{i18n.get('plugins_load_failed')}{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}{i18n.get('plugins_must_be_in', path=PLUGINS_DIR)}{Style.RESET_ALL}")
            else:
                print(f"\n  {Fore.YELLOW}{i18n.get('plugins_loading_from', path=path)}{Style.RESET_ALL}")
                confirm = input(f"  {i18n.get('plugins_confirm_load', default='Continue? (Y/N)')} ").strip().upper()
                if confirm == "Y":
                    info = register_plugin(path)
                    if info:
                        print(f"\n  {Fore.GREEN}{i18n.get('plugins_loaded', name=info['name'], extensions=info.get('extensions', []))}{Style.RESET_ALL}")
                    else:
                        print(f"\n  {Fore.RED}{i18n.get('plugins_load_failed')}{Style.RESET_ALL}")
            input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "2":
            if plugins:
                print(f"\n  {i18n.get('plugins_enter_unload')}")
                name = input("  > ").strip()
                if unregister_plugin(name):
                    print(f"\n  {Fore.GREEN}{i18n.get('plugins_unloaded', name=name)}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.RED}{i18n.get('plugins_not_found')}{Style.RESET_ALL}")
            input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
