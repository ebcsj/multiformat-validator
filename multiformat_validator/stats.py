import re
from pathlib import Path


COMMENT_PATTERNS = {
    ".py": (r'^\s*#', r'"""', r"'''"),
    ".js": (r'^\s*//', r'/\*', r'\*/'),
    ".ts": (r'^\s*//', r'/\*', r'\*/'),
    ".jsx": (r'^\s*//', r'/\*', r'\*/'),
    ".tsx": (r'^\s*//', r'/\*', r'\*/'),
    ".java": (r'^\s*//', r'/\*', r'\*/'),
    ".cs": (r'^\s*//', r'/\*', r'\*/'),
    ".go": (r'^\s*//', r'/\*', r'\*/'),
    ".rb": (r'^\s*#', None, None),
    ".rs": (r'^\s*//', r'/\*', r'\*/'),
    ".kt": (r'^\s*//', r'/\*', r'\*/'),
    ".swift": (r'^\s*//', r'/\*', r'\*/'),
    ".php": (r'^\s*//', r'/\*', r'\*/'),
    ".lua": (r'^\s*--', None, None),
    ".pl": (r'^\s*#', None, None),
    ".scala": (r'^\s*//', r'/\*', r'\*/'),
    ".html": (r'<!--', r'<!--', r'-->'),
    ".css": (r'^\s*//', r'/\*', r'\*/'),
    ".md": (None, None, None),
    ".sql": (r'^\s*--', r'/\*', r'\*/'),
    ".sh": (r'^\s*#', None, None),
    ".bat": (r'^\s*rem', r'^\s*::', None),
    ".ini": (r'^\s*[;#]', None, None),
    ".yaml": (r'^\s*#', None, None),
    ".yml": (r'^\s*#', None, None),
    ".json": (None, None, None),
    ".xml": (r'<!--', r'<!--', r'-->'),
}


def count_lines(file_path: str) -> dict:
    path = Path(file_path)
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"total": 0, "code": 0, "comments": 0, "blank": 0}

    lines = content.split("\n")
    total = len(lines)
    blank = sum(1 for line in lines if line.strip() == "")

    ext = path.suffix.lower()
    patterns = COMMENT_PATTERNS.get(ext, (None, None, None))
    single_comment = patterns[0]

    comments = 0
    in_block = False
    block_end = patterns[2] if patterns[2] else ""

    for line in lines:
        stripped = line.strip()
        if in_block:
            comments += 1
            if block_end and block_end in stripped:
                in_block = False
        elif patterns[1] and patterns[1] in stripped:
            comments += 1
            if block_end and block_end not in stripped:
                in_block = True
        elif single_comment and re.match(single_comment, line):
            comments += 1

    code = total - blank - comments
    ratio = f"{(comments / total * 100):.1f}%" if total > 0 else "0%"

    return {
        "total": total,
        "code": code,
        "comments": comments,
        "blank": blank,
        "ratio": ratio,
        "ext": ext,
    }


def scan_folder_stats(folder_path: str, recursive: bool = True) -> dict:
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return {"files": 0, "total": 0, "code": 0, "comments": 0, "blank": 0, "languages": {}}

    iterator = folder.rglob("*") if recursive else folder.glob("*")
    stats = {"files": 0, "total": 0, "code": 0, "comments": 0, "blank": 0, "languages": {}}

    for file_path in iterator:
        if file_path.is_file() and file_path.suffix.lower() in COMMENT_PATTERNS:
            result = count_lines(str(file_path))
            if result["total"] > 0:
                stats["files"] += 1
                stats["total"] += result["total"]
                stats["code"] += result["code"]
                stats["comments"] += result["comments"]
                stats["blank"] += result["blank"]
                ext = result["ext"]
                if ext not in stats["languages"]:
                    stats["languages"][ext] = {"files": 0, "lines": 0}
                stats["languages"][ext]["files"] += 1
                stats["languages"][ext]["lines"] += result["total"]

    return stats
