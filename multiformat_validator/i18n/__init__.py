import json
from pathlib import Path


LANGUAGES = {
    "1": "zh_TW",
    "2": "zh_CN",
    "3": "en",
    "4": "ja",
    "5": "ko",
}


class I18n:
    def __init__(self, lang_code: str):
        self.lang_code = lang_code
        self.strings = self._load_strings()
        self.en_strings = self._load_en_strings() if lang_code != "en" else self.strings

    def _load_strings(self) -> dict:
        i18n_dir = Path(__file__).parent
        json_file = i18n_dir / f"{self.lang_code}.json"
        with open(json_file, encoding="utf-8") as f:
            return json.load(f)

    def _load_en_strings(self) -> dict:
        i18n_dir = Path(__file__).parent
        json_file = i18n_dir / "en.json"
        with open(json_file, encoding="utf-8") as f:
            return json.load(f)

    def get(self, key: str, **kwargs) -> str:
        template = self.strings.get(key)
        if template is None:
            template = self.en_strings.get(key, key)
        if kwargs:
            return template.format(**kwargs)
        return template
