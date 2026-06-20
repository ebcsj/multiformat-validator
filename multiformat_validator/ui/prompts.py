import os


_i18n_cache = None


def _get_i18n():
    global _i18n_cache
    if _i18n_cache is None:
        from ..i18n import I18n
        from ..config import load_config
        _i18n_cache = I18n(load_config().get("language", "en"))
    return _i18n_cache


def get_safe_choice(prompt: str, valid_choices: list[str]) -> str:
    while True:
        try:
            choice = input(prompt).strip().upper()
            if choice in valid_choices:
                return choice
            print(f"  {_get_i18n().get('invalid_choice', choices=', '.join(valid_choices))}")
        except (EOFError, KeyboardInterrupt):
            return ""


def clean_path(path_str: str) -> str:
    cleaned = path_str.strip()
    if cleaned.startswith('"') and cleaned.endswith('"'):
        cleaned = cleaned[1:-1]
    if cleaned.startswith("'") and cleaned.endswith("'"):
        cleaned = cleaned[1:-1]
    cleaned = os.path.realpath(os.path.abspath(cleaned))
    return cleaned
