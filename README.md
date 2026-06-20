# MultiFormat Validator CLI

Professional multi-format syntax validation tool. Supports 63 file formats and 5 interface languages.

[View Changelog](CHANGELOG.md)

> **This project is now fully open-source!** We have received inquiries from schools interested in adopting this tool for educational purposes. To deliver a better experience, we are actively developing and working on adding more exciting features. Stay tuned!

## License

Copyright (c) 2026 MultiFormat Validator CLI - Kerby Chow. All rights reserved.

- **Allowed:** Personal, non-commercial, educational use; modifications and derivative works for personal use
- **Prohibited:** Commercial use, redistribution, selling
- **Share:** Official GitHub link only

Full license terms: [LICENSE](LICENSE)

## Why Use This Tool?

Developers often need to check syntax across different file formats. MultiFormat Validator CLI lets you:

- Validate 63 formats including JSON, Python, HTML, XML, BAT/CMD
- Use a familiar terminal interface
- Export professional HTML diagnostic reports

## Features

| Feature | Description |
|---------|-------------|
| Multi-language UI | Traditional Chinese, Simplified Chinese, English, Japanese, Korean |
| 63 Formats | JSON, Python, HTML, XML, PHP, CSS, Markdown, and more |
| Batch Scan | Recursively scan entire folders with streaming generator |
| Export Reports | HTML, JSON, CSV, TXT report formats with custom save path |
| Smart Encoding | Auto-detect UTF-8, GBK, Big5, and more |
| History | Auto-save last validated file path |
| Auto Fix | Basic syntax auto-repair with Diff preview |
| Custom Rules | Define validation rules with regex (ReDoS protected) |
| Plugin System | Load third-party validators (with path validation & hash verification) |
| Right-click Menu | Validate files directly from Windows Explorer |
| Theme Support | Dark and Light theme with instant switching |
| File Browser | Interactive browser with direct path input |
| Error Detection | Clear messages for empty files, missing files, encoding errors |
| Security | Sandboxed validators, XXE protection, path protection, thread-safe |
| Log Rotation | Automatic log file rotation (5MB max, 3 backups) |
| Config Validation | Automatic config value type/range validation |

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.12 or above |
| colorama | >= 0.4.6 |
| pyyaml | (optional) For YAML validation |

## Installation

### Easiest Way (Recommended for Beginners)

1. Download this project
2. Open the folder
3. Double-click `install.bat`
4. Select `[1] Install` and wait for completion
5. Done! Type `check-cli` in terminal to start

### Method 2: Manual Installation

```bash
# 1. Clone the project
git clone <repo-url>
cd "CLI Making"

# 2. Install package
pip install -e .

# 3. Verify installation
check-cli --version
```

### Method 3: Without Modifying PATH

```bash
# Run directly from project directory
check-cli.bat

# Or use Python module
python -m multiformat_validator
```

## Usage

### Interactive Mode

```bash
check-cli
```

After starting, select language (1-5), then use the main menu:

| Option | Function | Description |
|--------|----------|-------------|
| `[0]` | Quick retry | Re-validate the last file you checked |
| `[1]` | Check single file | Enter a file path to validate |
| `[2]` | Batch scan | Scan all files in a folder recursively |
| `[3]` | File browser | Browse folders and select files interactively |
| `[4]` | Compare files | Compare validation results of two files |
| `[5]` | Batch export | Export scan results to JSON/CSV/TXT/HTML |
| `[6]` | Templates | Save/load/delete validation templates |
| `[7]` | Statistics | Count lines, comments, and blank lines |
| `[8]` | History | View and manage validation history |
| `[9]` | Custom validators | Create/delete custom validation rules |
| `[R]` | Custom rules | Define regex-based validation rules |
| `[P]` | Plugins | Load/unload third-party validator plugins |
| `[Q]` | Quick validate | Install right-click context menu (Windows) |
| `[S]` | Settings | Change language, theme, logging, etc. |
| `[H]` | Help | Show help and usage information |
| `[X]` | Exit | Exit the program |

#### Option 1: Validate Single File

1. Select `[1]` from main menu
2. Paste the file path (right-click to paste in terminal)
3. View the validation report
4. If errors found, option to auto-fix or export HTML report

#### Option 2: Batch Scan Folder

1. Select `[2]` from main menu
2. Enter the folder path
3. View all file results at once
4. Option to export JSON/CSV/TXT/HTML report with custom save path

#### Option 3: File Browser

1. Select `[3]` from main menu
2. Navigate directories by entering numbers, or enter a full path to jump directly
3. Select a file to validate

#### Option 8: History

1. Select `[8]` from main menu
2. View recent validation records
3. Option to export or clear history

### CLI Arguments

```bash
check-cli <file>                     # Validate file
check-cli <folder> -r                # Recursive scan
check-cli -l zh_TW <file>           # Set language
check-cli -f json -o out.json       # Export JSON report
check-cli -f csv -o out.csv         # Export CSV report
check-cli -f txt -o out.txt         # Export TXT report
check-cli -f html -o out.html       # Export HTML report
check-cli --list-formats             # List all supported formats
check-cli --version                  # Show version
```

### Interactive Mode - Batch Export

When using batch scan (option `[2]`), you can choose to export results:

```
Export format (JSON/CSV/TXT/HTML)：JSON

Enter output file path (leave empty for default location):
> C:\Users\YourName\Desktop\my_report.json

  Saved to: C:\Users\YourName\Desktop\my_report.json
```

- Leave the path **empty** to save in current directory as `batch_report.<format>`
- Enter a **full path** to save anywhere you want

### CLI Arguments Reference

| Argument | Options | Description |
|----------|---------|-------------|
| `path` | — | File or folder path |
| `-l, --lang` | `zh_TW`, `zh_CN`, `en`, `ja`, `ko` | Interface language (default: en) |
| `-f, --format` | `text`, `json`, `csv`, `txt`, `html` | Output format (default: text) |
| `-o, --output` | file path | Output file path |
| `-r, --recursive` | — | Scan folder recursively |
| `--list-formats` | — | List all supported formats |
| `--version` | — | Show version |

## Configuration

Config file location: `~/.multiformat_validator/preferences.json`

```json
{
  "language": "en",
  "output_format": "text",
  "theme": "dark",
  "exclude_patterns": ["node_modules", ".git", "__pycache__", ".venv"],
  "max_file_size_mb": 10,
  "logging_enabled": false,
  "parallel_scanning": false,
  "parallel_workers": 4
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `language` | `"en"` | Interface language |
| `output_format` | `"text"` | Output format |
| `theme` | `"dark"` | Theme style |
| `exclude_patterns` | `["node_modules", ...]` | Folders to exclude |
| `max_file_size_mb` | `10` | Max file size (MB) |
| `logging_enabled` | `false` | Enable logging |
| `parallel_scanning` | `false` | Enable parallel scanning |
| `parallel_workers` | `4` | Number of parallel threads |

## Project Structure

The codebase is organized into modular components for maintainability:

```
multiformat_validator/
├── cli.py                    # Entry point (<100 lines)
├── commands/                 # Command modules
│   ├── __init__.py          # Command routing
│   ├── validate.py          # Single file validation
│   ├── batch_scan.py        # Batch folder scanning
│   ├── compare.py           # File comparison
│   └── export.py            # Batch export
├── ui/                       # User interface
│   ├── menus.py             # Interactive menu system
│   ├── display.py           # Display functions
│   └── prompts.py           # User input handling
├── config/                   # Configuration management
│   ├── settings.py          # Settings menu
│   └── templates.py         # Template management
├── i18n/                     # Internationalization (5 languages)
├── validators/               # 25 format-specific validators
└── ...                       # Other modules (scanner, exporter, etc.)
```

## Supported Formats

### Configuration Files

| Format | Extensions |
|--------|------------|
| JSON | `.json` `.ipynb` `.jsonl` `.topojson` `.geojson` |
| YAML | `.yaml` `.yml` |
| INI | `.ini` `.properties` `.conf` `.cfg` `.prefs` `.inf` |
| XML | `.xml` `.xsd` `.rss` `.svg` `.plist` `.config` `.wsdl` |

### Programming Languages

| Format | Extensions |
|--------|------------|
| Python | `.py` `.pyw` `.pyi` `.pyx` |
| JavaScript | `.js` `.jsx` |
| TypeScript | `.ts` `.tsx` |
| Java | `.java` |
| C# | `.cs` |
| Go | `.go` |
| Ruby | `.rb` |
| Rust | `.rs` |
| Kotlin | `.kt` |
| Swift | `.swift` |
| Perl | `.pl` `.pm` |
| Lua | `.lua` |
| Scala | `.scala` |

### Web

| Format | Extensions |
|--------|------------|
| HTML | `.html` `.htm` `.xhtml` `.phtml` `.jsp` `.asp` `.aspx` |
| CSS | `.css` `.wxss` |
| PHP | `.php` `.php3` `.php4` `.php5` `.phps` |

### Markup Languages

| Format | Extensions |
|--------|------------|
| Markdown | `.md` `.markdown` `.mdown` `.mdwn` `.mkd` `.mkdn` |

### Scripts & Databases

| Format | Extensions |
|--------|------------|
| BAT/CMD | `.bat` `.cmd` `.nt` |
| SQL | `.sql` |

**Total: 63 extensions**

## Security

MultiFormat Validator CLI includes the following security measures:

| Feature | Description |
|---------|-------------|
| Sandboxed Validators | Custom validators run in restricted environment with limited builtins |
| Static Code Analysis | AST parsing blocks dangerous operations (import, exec, eval, open) |
| Plugin Path Validation | Plugins must reside in `~/.multiformat_validator/plugins/` |
| Plugin Hash Verification | SHA-256 checksums detect plugin tampering |
| Path Traversal Protection | All file paths are normalized; system directories are protected |
| XML XXE Protection | SAX parser with external entity loading disabled |
| ReDoS Protection | Regex matching limited to 1000 chars per line |
| Auto-fix Backup | Creates .bak file before applying fixes |
| Thread Safety | File operations use locks to prevent race conditions |
| Graceful Error Handling | PermissionError, FileNotFoundError handled without crashes |

For detailed security information, see [SECURITY.md](SECURITY.md).

## Troubleshooting

### Installation Issues

**Q: `check-cli` command not recognized?**

The `check-cli` command is installed to Python's Scripts folder, which may not be in your PATH.

Solution 1: Reinstall and add to PATH
```bash
pip install -e .
```

Solution 2: Use the batch file directly
```bash
check-cli.bat
```

Solution 3: Add Scripts folder to PATH (PowerShell)
```powershell
$old = [Environment]::GetEnvironmentVariable('Path','User')
[Environment]::SetEnvironmentVariable('Path', $old + ';C:\Users\YourName\AppData\Local\Python\pythoncore-3.14-64\Scripts','User')
```
Then restart your terminal.

**Q: `pip` command not found?**

Make sure Python is installed and added to PATH:
```bash
python --version
```
If not found, download Python from https://www.python.org/downloads/ and check "Add Python to PATH" during installation.

**Q: `install.bat` opens and closes immediately?**

This usually means Python is not installed. Install Python 3.12+ first, then run `install.bat` again.

### Usage Issues

**Q: Path contains spaces?**

Paste it directly, quotes are handled automatically:

```
> "C:\Program Files\config.json"
```

Do NOT drag and drop files into the terminal - this may cause path format issues. Use right-click to paste instead.

**Q: Encoding error or garbled text?**

The tool auto-detects encoding (UTF-8, GBK, Big5, etc.). If issues persist:
1. Open the file in a text editor
2. Save it as UTF-8 encoding
3. Try validating again

**Q: File not found error?**

Make sure you:
1. Use the full absolute path (e.g., `C:\Projects\file.json`)
2. Include the file extension
3. Use forward slashes or escaped backslashes

**Q: How to exclude specific folders from scanning?**

Edit `~/.multiformat_validator/preferences.json`:

```json
{
  "exclude_patterns": ["node_modules", ".git", "__pycache__", "vendor", "dist"]
}
```

**Q: File too large error?**

Default max size is 10 MB. To increase:
```json
{
  "max_file_size_mb": 50
}
```

**Q: How to change the default language?**

Edit `~/.multiformat_validator/preferences.json`:
```json
{
  "language": "zh_TW"
}
```
Available: `zh_TW`, `zh_CN`, `en`, `ja`, `ko`

**Q: How to change the theme?**

Edit `~/.multiformat_validator/preferences.json`:
```json
{
  "theme": "light"
}
```

### Report Issues

**Q: HTML report has no styling?**

CSS is fully embedded in the HTML file. Open it with a modern browser (Chrome, Firefox, Edge). The report is saved in the same folder as the validated file.

**Q: How to export reports?**

During validation, you'll be prompted to export. Or use CLI:
```bash
check-cli file.py -f json -o report.json
check-cli file.py -f csv -o report.csv
check-cli file.py -f txt -o report.txt
check-cli file.py -f html -o report.html
```

### Performance Issues

**Q: Scanning is slow?**

For large folders, enable parallel scanning:
```json
{
  "parallel_scanning": true,
  "parallel_workers": 4
}
```

**Q: How to enable logging?**

Edit `~/.multiformat_validator/preferences.json`:
```json
{
  "logging_enabled": true,
  "log_path": "validation.log"
}
```

### Other Issues

**Q: How to reset all settings?**

Delete the config file or reset it:
```bash
# Delete config
rm ~/.multiformat_validator/preferences.json

# Or use the settings menu in the tool
# Select [S] Settings > [C] Config > [7] Reset
```

**Q: How to view validation history?**

Select `[8]` from the main menu, or find the history file:
```
~/.multiformat_validator/.validation_history.json
```

**Q: How to uninstall?**

```bash
pip uninstall multiformat-validator
```
Then delete the project folder.

