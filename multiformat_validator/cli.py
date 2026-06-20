import argparse
from collections import defaultdict

from colorama import init
from . import __version__
from .validators import VALIDATORS
from .config import load_config, init_config
from .ui.prompts import clean_path

init(autoreset=True)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="check-cli",
        description=f"MultiFormat Validator CLI - Validate {len(VALIDATORS)} file formats",
    )
    parser.add_argument("path", nargs="?", help="File or folder path to validate")
    parser.add_argument("-l", "--lang", choices=["zh_TW", "zh_CN", "en", "ja", "ko"], default="en", help="Language (default: en)")
    parser.add_argument("-f", "--format", choices=["text", "json", "csv", "html", "txt"], default="text", help="Output format (default: text)")
    parser.add_argument("-o", "--output", help="Output file path for export")
    parser.add_argument("-r", "--recursive", action="store_true", help="Scan folder recursively")
    parser.add_argument("--list-formats", action="store_true", help="List all supported formats")
    parser.add_argument("--version", action="version", version=f"MultiFormat Validator CLI v{__version__}")
    return parser.parse_args(argv)


def list_formats(i18n=None, lang="en"):
    if i18n is None:
        from .i18n import I18n
        i18n = I18n(lang)

    groups = defaultdict(list)
    format_map = {
        ".json": "JSON", ".ipynb": "JSON", ".jsonl": "JSON", ".topojson": "JSON", ".geojson": "JSON",
        ".py": "Python", ".pyw": "Python", ".pyi": "Python", ".pyx": "Python",
        ".html": "HTML", ".htm": "HTML", ".xhtml": "HTML", ".phtml": "HTML", ".jsp": "HTML", ".asp": "HTML", ".aspx": "HTML",
        ".xml": "XML", ".xsd": "XML", ".rss": "XML", ".svg": "XML", ".plist": "XML", ".config": "XML", ".wsdl": "XML",
        ".bat": "BAT/CMD", ".cmd": "BAT/CMD", ".nt": "BAT/CMD",
        ".php": "PHP", ".php3": "PHP", ".php4": "PHP", ".php5": "PHP", ".phps": "PHP",
        ".css": "CSS", ".wxss": "CSS",
        ".md": "Markdown", ".markdown": "Markdown", ".mdown": "Markdown", ".mdwn": "Markdown", ".mkd": "Markdown", ".mkdn": "Markdown",
        ".ini": "INI", ".properties": "INI", ".conf": "INI", ".cfg": "INI", ".prefs": "INI", ".inf": "INI",
        ".js": "JavaScript", ".jsx": "JavaScript",
        ".ts": "TypeScript", ".tsx": "TypeScript",
        ".java": "Java", ".cs": "C#", ".go": "Go", ".rb": "Ruby", ".rs": "Rust",
        ".kt": "Kotlin", ".swift": "Swift", ".pl": "Perl", ".pm": "Perl",
        ".lua": "Lua", ".scala": "Scala", ".yml": "YAML", ".yaml": "YAML", ".sql": "SQL",
    }
    for ext in sorted(VALIDATORS.keys()):
        group = format_map.get(ext, "Unknown")
        groups[group].append(ext)

    print(f"\n{i18n.get('list_formats_title')}")
    print("=" * 50)
    for group in sorted(groups.keys()):
        extensions = ", ".join(groups[group])
        print(f"  {group}: {extensions}")
    print(f"\n{i18n.get('list_formats_total', count=len(VALIDATORS))}")


def cli_mode(args):
    config = load_config()

    if args.list_formats:
        lang = args.lang if args.lang != "en" else config.get("language", "en")
        from .i18n import I18n
        list_formats(I18n(lang))
        return

    if not args.path:
        from .i18n import I18n
        from .ui.menus import interactive_mode
        lang = args.lang if args.lang != "en" else config.get("language", "en")
        interactive_mode(I18n(lang), config)
        return

    from .commands import route_command
    route_command(args)


def _check_path_warning():
    import sys
    import os
    import shutil

    exe = shutil.which("check-cli")
    if exe is not None:
        return
    scripts_dir = os.path.dirname(sys.executable)
    if scripts_dir.lower().endswith("scripts"):
        pass
    else:
        return
    path_env = os.environ.get("PATH", "")
    for p in path_env.split(os.pathsep):
        if os.path.normcase(os.path.normpath(p)) == os.path.normcase(os.path.normpath(scripts_dir)):
            return
    from .i18n import I18n
    from .config import load_config
    cfg = load_config()
    _i18n = I18n(cfg.get("language", "en"))
    print(f"  {_i18n.get('warning_path_not_set', path=scripts_dir)}")
    print()


def main():
    import sys

    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

    try:
        init_config()
        _check_path_warning()
        args = parse_args()
        cli_mode(args)
    except KeyboardInterrupt:
        from .i18n import I18n
        from .config import load_config
        cfg = load_config()
        _i18n = I18n(cfg.get("language", "en"))
        print(f"\n\n[!] {_i18n.get('user_cancelled')}")
        sys.exit(0)


if __name__ == "__main__":
    main()
