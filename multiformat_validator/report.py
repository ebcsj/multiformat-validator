from pathlib import Path
from html import escape


def generate_html_report(result: dict, file_path: str, i18n, output_dir: str = None, filename: str = "report.html") -> str:
    report_dir = Path(output_dir) if output_dir else Path(file_path).parent
    report_path = report_dir / filename

    errors_html = ""
    for error in result["errors"]:
        errors_html += f"""
        <div class="error-card">
            <div class="error-header">
                <span class="glow-label glow-red">{escape(str(error['type']))}</span>
                <span class="glow-label glow-yellow">{i18n.get('error_line')}: {error['line']}</span>
                <span class="glow-label glow-cyan">{i18n.get('error_col')}: {error['col']}</span>
            </div>
            <div class="error-message">{escape(str(error['message']))}</div>
            <div class="error-fix">{i18n.get('error_fix')}: {escape(str(error['fix']))}</div>
        </div>
"""

    html_lang = i18n.lang_code if hasattr(i18n, 'lang_code') else "en"
    html = f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{i18n.get('report_title')} - {Path(file_path).name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .glass-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        .header .file-path {{
            color: rgba(255, 255, 255, 0.5);
            font-size: 14px;
        }}
        .status-badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        .status-failed {{
            background: rgba(255, 71, 87, 0.2);
            border: 1px solid rgba(255, 71, 87, 0.5);
            color: #ff4757;
        }}
        .error-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            transition: transform 0.2s;
        }}
        .error-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.15);
        }}
        .error-header {{
            display: flex;
            gap: 10px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}
        .glow-label {{
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .glow-red {{
            background: rgba(255, 71, 87, 0.15);
            border: 1px solid rgba(255, 71, 87, 0.4);
            color: #ff6b81;
            box-shadow: 0 0 10px rgba(255, 71, 87, 0.2);
        }}
        .glow-yellow {{
            background: rgba(254, 202, 87, 0.15);
            border: 1px solid rgba(254, 202, 87, 0.4);
            color: #feca57;
            box-shadow: 0 0 10px rgba(254, 202, 87, 0.2);
        }}
        .glow-cyan {{
            background: rgba(72, 219, 251, 0.15);
            border: 1px solid rgba(72, 219, 251, 0.4);
            color: #48dbfb;
            box-shadow: 0 0 10px rgba(72, 219, 251, 0.2);
        }}
        .error-message {{
            font-size: 15px;
            color: #d1d1d1;
            margin-bottom: 10px;
            line-height: 1.5;
        }}
        .error-fix {{
            font-size: 13px;
            color: #7bed9f;
            font-weight: 600;
            padding: 8px 12px;
            background: rgba(123, 237, 159, 0.08);
            border-radius: 8px;
            border-left: 3px solid #7bed9f;
        }}
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.3);
            font-size: 12px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="glass-card header">
            <h1>{i18n.get('report_title')}</h1>
            <div class="file-path">{escape(file_path)}</div>
        </div>
        <div class="glass-card">
            <span class="status-badge status-failed">{i18n.get('validation_failed')}</span>
            {errors_html}
        </div>
        <div class="footer">{i18n.get('app_name')}</div>
    </div>
</body>
</html>"""

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(html, encoding="utf-8")
    return str(report_path)


def generate_comparison_report(results: list[dict], i18n, output_dir: str = ".", filename: str = "batch_report.html") -> str:
    total = len(results)
    valid_count = sum(1 for r in results if r.get("valid", False))
    invalid_count = total - valid_count
    pass_rate = (valid_count / total * 100) if total > 0 else 0

    error_types: dict[str, int] = {}
    for r in results:
        for e in r.get("errors", []):
            t = e.get("type", "Unknown")
            error_types[t] = error_types.get(t, 0) + 1

    sorted_types = sorted(error_types.items(), key=lambda x: -x[1])
    max_count = max(error_types.values()) if error_types else 1

    type_bars_html = ""
    for t, count in sorted_types:
        pct = count / max_count * 100
        type_bars_html += f"""
            <div class="bar-row">
                <span class="bar-label">{escape(t)}</span>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{pct}%"></div>
                </div>
                <span class="bar-value">{count}</span>
            </div>"""

    pass_text = i18n.get('history_pass')
    fail_text = i18n.get('history_fail')

    files_html = ""
    for r in results:
        status_class = "status-pass" if r.get("valid") else "status-fail"
        status_text = pass_text if r.get("valid") else fail_text
        error_count = len(r.get("errors", []))
        files_html += f"""
            <tr>
                <td class="file-name">{escape(r.get('file', ''))}</td>
                <td><span class="status-badge-sm {status_class}">{status_text}</span></td>
                <td class="error-num">{error_count}</td>
            </tr>"""

    severity_map = {"error": 0, "warning": 0, "info": 0}
    for r in results:
        for e in r.get("errors", []):
            sev = e.get("severity", "error")
            if sev in severity_map:
                severity_map[sev] += 1
            else:
                severity_map["error"] += 1

    severity_html = ""
    sev_labels = {
        "error": i18n.get('report_severity_error'),
        "warning": i18n.get('report_severity_warning'),
        "info": i18n.get('report_severity_info'),
    }
    for sev, count in severity_map.items():
        if count > 0:
            sev_label = sev_labels.get(sev, sev.capitalize())
            severity_html += f"""
            <div class="severity-item">
                <span class="severity-dot severity-{sev}"></span>
                <span>{sev_label}: {count}</span>
            </div>"""

    title = i18n.get('report_batch_title')
    total_label = i18n.get('total_files')
    valid_label = i18n.get('valid_files')
    invalid_label = i18n.get('invalid_files')
    pass_rate_label = i18n.get('report_pass_rate')
    error_dist_label = i18n.get('report_error_distribution')
    severity_label = i18n.get('report_severity_overview')
    file_details_label = i18n.get('report_file_details')
    file_th = i18n.get('report_file')
    status_th = i18n.get('report_status')
    errors_th = i18n.get('report_errors')
    generated_by = i18n.get('report_generated_by')

    html_lang = i18n.lang_code if hasattr(i18n, 'lang_code') else "en"
    html = f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
            padding: 40px 20px;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .glass-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
        }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{
            font-size: 28px;
            background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        .header .subtitle {{ color: rgba(255, 255, 255, 0.5); font-size: 14px; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 4px;
        }}
        .stat-label {{ font-size: 12px; color: rgba(255, 255, 255, 0.5); }}
        .stat-green {{ color: #7bed9f; }}
        .stat-red {{ color: #ff6b81; }}
        .stat-yellow {{ color: #feca57; }}
        .stat-cyan {{ color: #48dbfb; }}
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #feca57;
        }}
        .bar-row {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            gap: 12px;
        }}
        .bar-label {{
            width: 200px;
            font-size: 13px;
            text-align: right;
            color: rgba(255, 255, 255, 0.7);
        }}
        .bar-track {{
            flex: 1;
            height: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            overflow: hidden;
        }}
        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b, #feca57);
            border-radius: 10px;
            transition: width 0.3s;
        }}
        .bar-value {{
            width: 40px;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.7);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            text-align: left;
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 13px;
            color: rgba(255, 255, 255, 0.5);
            text-transform: uppercase;
        }}
        td {{
            padding: 10px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 14px;
        }}
        .file-name {{ color: #48dbfb; }}
        .error-num {{ text-align: center; color: #ff6b81; }}
        .status-badge-sm {{
            display: inline-block;
            padding: 2px 10px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
        }}
        .status-pass {{ background: rgba(123, 237, 159, 0.15); color: #7bed9f; }}
        .status-fail {{ background: rgba(255, 71, 87, 0.15); color: #ff6b81; }}
        .severity-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }}
        .severity-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}
        .severity-error {{ background: #ff6b81; }}
        .severity-warning {{ background: #feca57; }}
        .severity-info {{ background: #48dbfb; }}
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.3);
            font-size: 12px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="glass-card header">
            <h1>{title}</h1>
            <div class="subtitle">{i18n.get('app_name')}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value stat-cyan">{total}</div>
                <div class="stat-label">{total_label}</div>
            </div>
            <div class="stat-card">
                <div class="stat-value stat-green">{valid_count}</div>
                <div class="stat-label">{valid_label}</div>
            </div>
            <div class="stat-card">
                <div class="stat-value stat-red">{invalid_count}</div>
                <div class="stat-label">{invalid_label}</div>
            </div>
            <div class="stat-card">
                <div class="stat-value stat-yellow">{pass_rate:.1f}%</div>
                <div class="stat-label">{pass_rate_label}</div>
            </div>
        </div>

        {"<div class='glass-card'><div class='section-title'>" + error_dist_label + "</div>" + type_bars_html + "</div>" if type_bars_html else ""}

        {("<div class='glass-card'><div class='section-title'>" + severity_label + "</div>" + severity_html + "</div>") if severity_html else ""}

        <div class="glass-card">
            <div class="section-title">{file_details_label}</div>
            <table>
                <thead>
                    <tr>
                        <th>{file_th}</th>
                        <th>{status_th}</th>
                        <th style="text-align:center">{errors_th}</th>
                    </tr>
                </thead>
                <tbody>
                    {files_html}
                </tbody>
            </table>
        </div>

        <div class="footer">{generated_by}</div>
    </div>
</body>
</html>"""

    output_path = Path(output_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return str(output_path)
