import os
from pathlib import Path
from colorama import Fore, Style
from .validators import VALIDATORS


def browse_folder(current_path: str = ".", i18n=None) -> str | None:
    current = Path(current_path).resolve()

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('browser_title') if i18n else 'File Browser'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")
        print(f"  {Fore.WHITE}Current: {current}{Style.RESET_ALL}\n")

        items = []
        if current.parent != current:
            items.append(("..", "[DIR] Up"))

        try:
            dirs = sorted([d for d in current.iterdir() if d.is_dir() and not d.name.startswith(".")])
            files = sorted([f for f in current.iterdir() if f.is_file() and f.suffix.lower() in VALIDATORS])
        except PermissionError:
            print(f"  {Fore.RED}{i18n.get('browser_permission_denied', path=str(current)) if i18n else f'Permission denied: {current}'}{Style.RESET_ALL}")
            input(f"  {Fore.WHITE}{i18n.get('press_enter') if i18n else 'Press Enter to go back...'}{Style.RESET_ALL}")
            if current.parent != current:
                current = current.parent
            continue

        for d in dirs[:20]:
            items.append((d.name, "[DIR]"))

        for f in files[:20]:
            ext = f.suffix.lower()
            items.append((f.name, f"[{ext}]"))

        for idx, (name, desc) in enumerate(items, 1):
            if desc.startswith("[DIR]"):
                print(f"  {Fore.CYAN}{idx}. {name}/ {Style.RESET_ALL}{Fore.WHITE}{desc}{Style.RESET_ALL}")
            else:
                print(f"  {Fore.GREEN}{idx}. {name} {Style.RESET_ALL}{Fore.YELLOW}{desc}{Style.RESET_ALL}")

        if not items:
            print(f"  {Fore.RED}{i18n.get('browser_no_files') if i18n else 'No supported files found in this directory.'}{Style.RESET_ALL}")

        print(f"\n  {Fore.WHITE}{i18n.get('browser_prompt') if i18n else 'Enter number, full path, or q to quit:'}{Style.RESET_ALL}")
        choice = input("  > ").strip()

        if choice.lower() == "q":
            return None

        if not choice:
            continue

        input_path = Path(choice)
        if input_path.is_absolute():
            if input_path.is_file() and input_path.suffix.lower() in VALIDATORS:
                return str(input_path)
            elif input_path.is_dir():
                current = input_path.resolve()
                continue
            else:
                print(f"  {Fore.RED}{i18n.get('browser_invalid_path', path=choice) if i18n else f'Invalid path: {choice}'}{Style.RESET_ALL}")
                input(f"  {Fore.WHITE}{i18n.get('press_enter') if i18n else 'Press Enter...'}{Style.RESET_ALL}")
                continue
        elif ":" in choice and choice[1] == ":":
            if input_path.is_file() and input_path.suffix.lower() in VALIDATORS:
                return str(input_path)
            elif input_path.is_dir():
                current = input_path.resolve()
                continue
            else:
                print(f"  {Fore.RED}{i18n.get('browser_invalid_path', path=choice) if i18n else f'Invalid path: {choice}'}{Style.RESET_ALL}")
                input(f"  {Fore.WHITE}{i18n.get('press_enter') if i18n else 'Press Enter...'}{Style.RESET_ALL}")
                continue
        elif choice.startswith("~"):
            expanded = Path(choice).expanduser()
            if expanded.is_file() and expanded.suffix.lower() in VALIDATORS:
                return str(expanded)
            elif expanded.is_dir():
                current = expanded.resolve()
                continue
            else:
                print(f"  {Fore.RED}{i18n.get('browser_invalid_path', path=choice) if i18n else f'Invalid path: {choice}'}{Style.RESET_ALL}")
                input(f"  {Fore.WHITE}{i18n.get('press_enter') if i18n else 'Press Enter...'}{Style.RESET_ALL}")
                continue

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                selected = items[idx][0]
                if selected == "..":
                    current = current.parent
                elif items[idx][1].startswith("[DIR]"):
                    current = current / selected
                else:
                    return str(current / selected)
        except (ValueError, IndexError):
            print(f"  {Fore.RED}{i18n.get('browser_invalid_input') if i18n else 'Invalid input. Enter a number, path, or q.'}{Style.RESET_ALL}")
            input(f"  {Fore.WHITE}{i18n.get('press_enter') if i18n else 'Press Enter...'}{Style.RESET_ALL}")

    return None
