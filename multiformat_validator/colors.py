from colorama import Fore, Style

_current_theme = "dark"

DARK = {
    "header": Fore.CYAN,
    "title": Fore.YELLOW,
    "success": Fore.GREEN,
    "error": Fore.RED,
    "info": Fore.WHITE,
    "accent": Fore.BLUE,
    "muted": Fore.WHITE,
}

LIGHT = {
    "header": Fore.BLUE,
    "title": Fore.YELLOW,
    "success": Fore.GREEN,
    "error": Fore.RED,
    "info": Fore.BLACK,
    "accent": Fore.CYAN,
    "muted": Fore.BLACK,
}


def set_theme(theme: str):
    global _current_theme
    _current_theme = theme if theme in ("dark", "light") else "dark"


def get_theme() -> str:
    return _current_theme


def c() -> dict:
    return DARK if _current_theme == "dark" else LIGHT
