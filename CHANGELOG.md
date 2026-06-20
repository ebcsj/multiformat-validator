# Changelog

All notable changes to MultiFormat Validator CLI will be documented in this file.

## [11.0.0] - 2026-06-21

### Changed
- **commands/export.py**: HTML export passes user-specified filename
- **commands/batch_scan.py**: HTML export passes user-specified filename
- **README.md / README_zh.md**: Updated features table and documentation
- **Consolidated _scan_folder**: Unified into `commands/__init__.py`, removed duplicates
- **Simplified _validate_file**: Reduced exception handling from 8 blocks to 2
- **Updated Documentation**: README.md, README_zh.md, SECURITY.md fully updated

---

## [10.0.0] - 2026-06-15

### Added
- **Custom Export Path**: Batch scan and history export now ask for output path
- **HTML Export Path Selection**: Single file HTML report now asks for save location
- **PATH Warning**: Shows warning when `check-cli` is not on PATH

### Changed
- **batch_scan.py**: Export format prompt now shows JSON/CSV/TXT/HTML

---

## [9.0.0] - 2026-06-05

### Fixed
- **i18n**: Added report, browser, diff, theme, and plugin i18n keys
- **commands/__init__.py**: Fixed missing report path feedback for HTML export
- **i18n**: Fixed duplicate `plugins_loaded` key in all 5 language files

### Added
- **colors.py**: New theme-aware color module for dark/light theme support
- **Theme Support**: Dark and Light theme with instant switching
- **File Browser Path Input**: Directly enter full paths in file browser

---

## [8.0.0] - 2026-05-22

### Fixed
- **quick_validate.py**: Added i18n support for all status messages
- **exporter.py**: Added i18n support to CSV/TXT export headers
- **i18n**: Fixed missing `plugins_confirm_load` key
- **check-cli.bat**: Added py/python3 launcher support, removed Windows error message flash
- **install.bat**: Fixed incorrect config cleanup paths in uninstall

---

## [7.0.0] - 2026-05-13

### Fixed
- **report.py**: Fixed `<html lang="en">` to use i18n language code
- **report.py**: Fixed hardcoded product name with `i18n.get('app_name')`
- **browser.py**: Added i18n support for all user-facing strings
- **commands/validate.py**: Fixed hardcoded "Line" label with i18n


---

## [6.0.0] - 2026-05-11

### Fixed
- **ui/prompts.py**: Replaced hardcoded Chinese in invalid choice message with i18n
- **UTF-8 Encoding Protection**: Handles Windows cmd.exe with legacy codepages
- **Graceful Ctrl+C Exit**: KeyboardInterrupt caught with user-friendly message
- **Microsoft Store Python Detection**: Improved Python detection for Windows Store installs

---

## [5.0.0] - 2026-05-01

### Fixed
- **ui/menus.py**: Fixed `labels[theme]` KeyError bug in theme selection
- **parallel_scanner.py**: Added protected path check, symlink cycle detection, proper exclusion matching
- **commands/validate.py**: Unified encoding detection with `read_with_detection`
- **fixer.py**: Replaced hardcoded Chinese in `show_diff_preview` with i18n
- **cli.py**: Replaced hardcoded Chinese in KeyboardInterrupt message with i18n
- **display_batch_results i18n**: Replaced hardcoded English with i18n keys
- **_fix_json Useless Function**: Removed unused `_fix_json` that always returned None

---

## [4.0.0] - 2026-04-26

#### Performance
- **Streaming Generator**: Folder scanning uses `os.walk` generator for memory efficiency
- **Directory Pruning**: Excluded folders are skipped during traversal

#### UX Improvements
- **Input Validation**: Added `get_safe_choice()` helper for menu inputs
- **Parent Directory Creation**: Auto-creates output directories before writing

---

## [3.0.0] - 2026-04-20

### Added

#### Features
- **Config Validation**: Automatic config value type/range validation and auto-sanitization
- **i18n Fallback**: Missing translations automatically fall back to English
- **Python Version Hints**: Syntax errors show Python version compatibility information
- **TXT/HTML Export**: Batch export now supports TXT and HTML formats
- **Thread-safe Print**: Added `thread_safe_print()` for parallel scanning output
- **HTML/JSON/CSV/TXT report export**
- **Auto-detect encoding (UTF-8, GBK, Big5, etc.)**
- **Custom validators with sandboxed execution**
- **Plugin system with hash verification**
- **Windows Explorer context menu integration**
- **Template management**
- **Code statistics**
- **Validation history**

#### Sercurity
- **Auto-fix Backup**: Creates `.bak` file before applying fixes
- **Config Corruption Recovery**: Auto-resets corrupted config files
- **Symlink Loop Detection**: Tracks visited real paths to prevent infinite recursion
- **Path Parts Matching**: Exclude patterns use path segments, not substrings

### Fixed
- **export_txt Line Number Display**: Fixed line=0 not showing in text reports

### Changed
- **Consolidated clean_path**: Unified into `ui/prompts.py`, removed duplicates

### Removed
- **Duplicate Functions**: Removed duplicate `clean_path` and `_scan_folder` definitions
- **Unnecessary Files**: Cleaned up generated reports and cache files


---

## [2.0.0] - 2026-04-09

### Added

#### Features
- **Auto-fix Diff Preview**: Shows colorized diff before applying auto-fixes using `difflib`
- **Offline HTML Reports**: All CSS embedded, no external CDN dependencies
- **Log Rotation**: Automatic log file rotation with `RotatingFileHandler` (5MB max, 3 backups)


#### Security
- **XML XXE Protection**: SAX parser with external entity loading disabled
- **ReDoS Protection**: Regex matching limited to 1000 characters per line

---

## [1.0.0] - 2026-03-28

### Features
- 63 file format support
- 5 interface languages (zh_TW, zh_CN, en, ja, ko)
- Batch folder scanning

### Security
- Sandboxed custom validators
- Plugin path validation
- Thread-safe file operations
- Graceful error handling
