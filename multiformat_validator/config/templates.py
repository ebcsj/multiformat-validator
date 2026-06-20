import importlib.util
import os

from colorama import Fore, Style


def manage_templates(i18n, config):
    from ..display import clear_screen
    from ..templates import save_template, load_template, delete_template, list_templates

    config_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")
    spec = importlib.util.spec_from_file_location("_config_raw", config_py_path)
    cfg_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg_mod)

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
                    cfg_mod.save_config(config)
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
