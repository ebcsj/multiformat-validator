import importlib.util
import os
import sys

from colorama import Fore, Style


def _get_config_module():
    config_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")
    spec = importlib.util.spec_from_file_location("_config_raw", config_py_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def settings_menu(i18n, config):
    from ..display import clear_screen

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
            from ..history import clear_history
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
    from ..display import clear_screen
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
        _get_config_module().save_config(config)
        i18n = I18n(code)
        print(f"\n  {Fore.GREEN}{i18n.get('language_changed', lang=name)}{Style.RESET_ALL}")
        input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        return i18n, config

    return I18n(config.get("language", "en")), config


def change_output_format(config):
    from ..display import clear_screen
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
        _get_config_module().save_config(config)
        i18n = I18n(config.get("language", "en"))
        print(f"\n  {Fore.GREEN}{i18n.get('format_changed', format=formats[choice])}{Style.RESET_ALL}")
        input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")

    return config


def change_theme(config):
    from ..display import clear_screen
    from ..i18n import I18n

    clear_screen()
    i18n = I18n(config.get("language", "en"))
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('theme_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    themes = {"1": "dark", "2": "light"}
    labels = {"1": i18n.get('theme_dark'), "2": i18n.get('theme_light')}

    for num, theme in themes.items():
        marker = f"{Fore.GREEN} {i18n.get('current_marker')}" if config.get("theme") == theme else ""
        print(f"  {num}. {labels[num]}{marker}")

    print()
    choice = input("  > ").strip()

    if choice in themes:
        config["theme"] = themes[choice]
        _get_config_module().save_config(config)
        print(f"\n  {Fore.GREEN}{i18n.get('theme_changed', theme=themes[choice])}{Style.RESET_ALL}")
        input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")

    return config


def manage_ignore_errors(i18n, config):
    from ..display import clear_screen

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

    _get_config_module().save_config(config)
    print(f"\n  {Fore.GREEN}{i18n.get('rules_saved')}{Style.RESET_ALL}")
    input(f"  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
    return config


def toggle_logging(i18n, config):
    from ..display import clear_screen

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
        _get_config_module().save_config(config)
        print(f"\n  {Fore.GREEN}{i18n.get('log_enabled')}{Style.RESET_ALL}")
    elif choice == "2":
        config["logging_enabled"] = False
        _get_config_module().save_config(config)
        print(f"\n  {Fore.GREEN}{i18n.get('log_disabled')}{Style.RESET_ALL}")

    input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
    return config


def manage_config(i18n, config):
    from ..display import clear_screen
    cfg = _get_config_module()

    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('config_title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

        print(f"  {i18n.get('config_path')}: {cfg.get_config_path()}\n")
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
                exported = cfg.export_config(path)
                print(f"\n  {Fore.GREEN}{i18n.get('config_exported', path=exported)}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "3":
            print(f"\n  {i18n.get('config_enter_path')}")
            path = input("  > ").strip()
            if path:
                imported = cfg.import_config(path)
                if imported:
                    config = imported
                    print(f"\n  {Fore.GREEN}{i18n.get('config_imported')}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.RED}{i18n.get('config_import_failed')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "4":
            backup_path = cfg.backup_config()
            if backup_path:
                print(f"\n  {Fore.GREEN}{i18n.get('config_backed_up', path=backup_path)}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "5":
            backups = cfg.list_backups()
            if backups:
                print(f"\n  {i18n.get('config_available_backups')}")
                for b in backups:
                    print(f"    - {b}")
                print(f"\n  {i18n.get('config_enter_backup')}")
                name = input("  > ").strip()
                if cfg.restore_config(name):
                    config = cfg.load_config()
                    print(f"\n  {Fore.GREEN}{i18n.get('config_restored', name=name)}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.RED}{i18n.get('config_restore_failed')}{Style.RESET_ALL}")
            else:
                print(f"\n  {i18n.get('config_no_backups')}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "6":
            backups = cfg.list_backups()
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
            config = cfg.reset_config()
            print(f"\n  {Fore.GREEN}{i18n.get('config_reset_done')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "8":
            recent = cfg.get_recent_files()
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
            recent = cfg.get_recent_folders()
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
            cfg.clear_recent()
            print(f"\n  {Fore.GREEN}{i18n.get('config_recent_cleared')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")


def check_for_updates(i18n, config=None):
    from ..display import clear_screen
    from .. import __version__

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
    from ..display import clear_screen
    from .. import __version__
    from ..validators import VALIDATORS

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


def manage_plugins(i18n):
    from ..display import clear_screen
    from ..plugins import list_plugins, register_plugin, unregister_plugin, PLUGINS_DIR

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
            from ..ui.prompts import clean_path
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
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
        elif choice == "2":
            if plugins:
                print(f"\n  {i18n.get('plugins_enter_unload')}")
                name = input("  > ").strip()
                if unregister_plugin(name):
                    print(f"\n  {Fore.GREEN}{i18n.get('plugins_unloaded', name=name)}{Style.RESET_ALL}")
                else:
                    print(f"\n  {Fore.RED}{i18n.get('plugins_not_found')}{Style.RESET_ALL}")
            input(f"\n  {Fore.WHITE}{i18n.get('press_enter')}{Style.RESET_ALL}")
