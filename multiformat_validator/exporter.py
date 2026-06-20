import json
import csv
from pathlib import Path


def export_json(results: list[dict], output_path: str) -> str:
    valid_count = 0
    for r in results:
        if r["valid"]:
            valid_count += 1

    report = {
        "summary": {
            "total": len(results),
            "valid": valid_count,
            "invalid": len(results) - valid_count,
        },
        "results": results,
    }

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)


def export_csv(results: list[dict], output_path: str, i18n=None) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        h_file = i18n.get('report_file') if i18n else "File"
        h_status = i18n.get('report_status') if i18n else "Valid"
        h_err_count = i18n.get('report_errors') if i18n else "Error Count"
        h_err_types = i18n.get('report_error_distribution') if i18n else "Error Types"
        h_line = i18n.get('error_line') if i18n else "First Error Line"
        h_msg = i18n.get('error_message') if i18n else "First Error Message"
        writer.writerow([h_file, h_status, h_err_count, h_err_types, h_line, h_msg])

        for r in results:
            errors = r["errors"]
            error_count = len(errors)
            error_types = "; ".join(e["type"] for e in errors) if errors else ""
            first_line = errors[0]["line"] if errors else ""
            first_msg = errors[0]["message"] if errors else ""
            writer.writerow([r["file"], r["valid"], error_count, error_types, first_line, first_msg])

    return str(path)


def export_txt(results: list[dict], output_path: str, i18n=None) -> str:
    def _get(key, **kwargs):
        if i18n:
            return i18n.get(key, **kwargs) if kwargs else i18n.get(key)
        return key

    lines = []
    lines.append("=" * 60)
    lines.append(f"  {_get('report_batch_title')}")
    lines.append("=" * 60)
    lines.append("")

    total = len(results)
    valid_count = sum(1 for r in results if r["valid"])
    invalid_count = total - valid_count

    lines.append(f"  {_get('total_files')}:  {total}")
    lines.append(f"  {_get('valid_files')}:        {valid_count}")
    lines.append(f"  {_get('invalid_files')}:      {invalid_count}")
    lines.append("")
    lines.append("-" * 60)

    pass_text = _get('history_pass')
    fail_text = _get('history_fail')

    for r in results:
        status = pass_text if r["valid"] else fail_text
        lines.append(f"  [{status}] {r['file']}")

        if not r["valid"] and r["errors"]:
            for e in r["errors"]:
                lines.append(f"    - {e['type']}: {e['message']}")
                if e.get("line") is not None and e["line"] > 0:
                    lines.append(f"      {_get('error_line')} {e['line']}, {_get('error_col')} {e['col']}")
                if e.get("fix"):
                    lines.append(f"      {_get('error_fix')}: {e['fix']}")
        lines.append("")

    lines.append("=" * 60)
    lines.append(f"  {_get('report_generated_by')}")
    lines.append("=" * 60)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)
