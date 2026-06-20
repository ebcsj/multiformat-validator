from pathlib import Path


ENCODING_PRIORITY = ["utf-8", "gbk", "big5", "utf-16", "latin-1"]


def detect_encoding(file_path: str) -> str:
    try:
        content = Path(file_path).read_bytes()
    except (PermissionError, FileNotFoundError, OSError):
        return "unknown"

    if not content:
        return "utf-8"

    if content[:3] == b"\xef\xbb\xbf":
        return "utf-8-sig"
    if content[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return "utf-16"
    if content[:4] in (b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff"):
        return "utf-32"

    for enc in ENCODING_PRIORITY:
        try:
            content.decode(enc)
            return enc
        except UnicodeDecodeError:
            continue

    return "unknown"


def read_with_detection(file_path: str) -> tuple[str, str]:
    try:
        encoding = detect_encoding(file_path)
    except Exception:
        encoding = "unknown"

    if encoding == "unknown":
        for enc in ENCODING_PRIORITY:
            try:
                content = Path(file_path).read_text(encoding=enc)
                return content, enc
            except (UnicodeDecodeError, PermissionError, FileNotFoundError, OSError):
                continue
        try:
            content = Path(file_path).read_bytes().decode("latin-1", errors="replace")
            return content, "latin-1"
        except Exception:
            return "", "unknown"

    try:
        content = Path(file_path).read_text(encoding=encoding)
        return content, encoding
    except (UnicodeDecodeError, PermissionError, FileNotFoundError, OSError):
        for enc in ENCODING_PRIORITY:
            try:
                content = Path(file_path).read_text(encoding=enc)
                return content, enc
            except (UnicodeDecodeError, PermissionError, FileNotFoundError, OSError):
                continue
        try:
            content = Path(file_path).read_bytes().decode("latin-1", errors="replace")
            return content, "latin-1"
        except Exception:
            return "", "unknown"
