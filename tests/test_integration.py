import os
import json
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestFullImportChain:
    def test_cli_package_imports(self):
        from multiformat_validator import cli, __version__
        assert __version__
        assert callable(cli.main)
        assert callable(cli.parse_args)
        assert callable(cli.clean_path)
        assert callable(cli.list_formats)
        assert callable(cli.cli_mode)

    def test_commands_package_imports(self):
        from multiformat_validator.commands import (
            route_command, run_validate, run_batch_scan, run_compare, run_export
        )
        assert callable(route_command)
        assert callable(run_validate)
        assert callable(run_batch_scan)
        assert callable(run_compare)
        assert callable(run_export)

    def test_ui_package_imports(self):
        from multiformat_validator.ui import interactive_mode, clean_path
        assert callable(interactive_mode)
        assert callable(clean_path)

    def test_config_package_imports(self):
        from multiformat_validator.config import (
            settings_menu, change_language, change_output_format, change_theme,
            manage_ignore_errors, toggle_logging, manage_config,
            check_for_updates, show_version_info, manage_plugins,
            manage_templates, load_config, save_config, reset_config,
            backup_config, restore_config, list_backups, export_config,
            import_config, add_recent_file, add_recent_folder,
            get_recent_files, get_recent_folders, clear_recent,
            get_config_path, init_config,
            CONFIG_DIR, CONFIG_FILE, BACKUP_DIR, DEFAULT_CONFIG,
        )
        assert callable(load_config)
        assert callable(save_config)
        assert callable(reset_config)
        assert callable(backup_config)
        assert callable(init_config)
        assert isinstance(DEFAULT_CONFIG, dict)

    def test_validators_package_imports(self):
        from multiformat_validator.validators import VALIDATORS
        assert isinstance(VALIDATORS, dict)
        assert len(VALIDATORS) > 0

    def test_scanner_imports(self):
        from multiformat_validator.scanner import scan_folder
        from multiformat_validator.parallel_scanner import scan_folder_parallel
        assert callable(scan_folder)
        assert callable(scan_folder_parallel)

    def test_core_module_imports(self):
        from multiformat_validator.encoder import read_with_detection
        from multiformat_validator.file_validation import validate_content
        from multiformat_validator.fixer import try_fix, apply_fixes
        from multiformat_validator.display import clear_screen, show_progress_bar
        from multiformat_validator.history import save_last_path
        from multiformat_validator.history_viewer import add_record
        from multiformat_validator.exporter import export_json, export_csv, export_txt
        from multiformat_validator.report import generate_html_report
        from multiformat_validator.stats import count_lines
        from multiformat_validator.browser import browse_folder
        from multiformat_validator.i18n import I18n
        assert callable(read_with_detection)
        assert callable(validate_content)
        assert callable(try_fix)
        assert callable(apply_fixes)
        assert callable(export_json)
        assert callable(export_csv)
        assert callable(export_txt)
        assert callable(generate_html_report)
        assert callable(count_lines)
        assert callable(browse_folder)

    def test_rules_plugins_imports(self):
        from multiformat_validator.rules_engine import check_custom_rules, load_rules, save_rule
        from multiformat_validator.plugins import list_plugins, get_plugin_validators, register_plugin
        from multiformat_validator.custom_validators import list_validators, save_validator, run_validator
        from multiformat_validator.templates import save_template, load_template
        assert callable(check_custom_rules)
        assert callable(list_plugins)
        assert callable(get_plugin_validators)
        assert callable(list_validators)


class TestConfigIntegration:
    def test_init_config_creates_directory(self):
        from multiformat_validator.config import init_config, CONFIG_FILE
        init_config()
        assert CONFIG_FILE.exists()

    def test_load_save_config_roundtrip(self):
        from multiformat_validator.config import load_config, save_config, reset_config
        reset_config()
        config = load_config()
        assert config["language"] == "en"
        config["language"] = "zh_CN"
        save_config(config)
        loaded = load_config()
        assert loaded["language"] == "zh_CN"
        reset_config()

    def test_backup_restore_roundtrip(self):
        from multiformat_validator.config import (
            load_config, save_config, backup_config, restore_config,
            list_backups, reset_config
        )
        reset_config()
        config = load_config()
        config["language"] = "ja"
        save_config(config)
        backup_name = backup_config()
        assert backup_name is not None
        backups = list_backups()
        assert len(backups) > 0
        config["language"] = "en"
        save_config(config)
        restored = restore_config(backup_name)
        assert restored is True
        loaded = load_config()
        assert loaded["language"] == "ja"
        reset_config()

    def test_export_import_config_roundtrip(self):
        from multiformat_validator.config import (
            load_config, save_config, export_config, import_config, reset_config
        )
        reset_config()
        config = load_config()
        config["theme"] = "light"
        save_config(config)
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            tmp_path = f.name
        try:
            export_config(tmp_path)
            config["theme"] = "dark"
            save_config(config)
            imported = import_config(tmp_path)
            assert imported is not None
            assert imported["theme"] == "light"
        finally:
            os.unlink(tmp_path)
        reset_config()

    def test_recent_files_management(self):
        from multiformat_validator.config import (
            add_recent_file, get_recent_files, clear_recent, reset_config
        )
        reset_config()
        add_recent_file("/tmp/test1.py")
        add_recent_file("/tmp/test2.py")
        recent = get_recent_files()
        assert "/tmp/test1.py" in recent
        assert "/tmp/test2.py" in recent
        assert recent[0] == "/tmp/test2.py"
        clear_recent()
        assert get_recent_files() == []
        reset_config()

    def test_recent_folders_management(self):
        from multiformat_validator.config import (
            add_recent_folder, get_recent_folders, clear_recent, reset_config
        )
        reset_config()
        add_recent_folder("/tmp/project1")
        add_recent_folder("/tmp/project2")
        recent = get_recent_folders()
        assert "/tmp/project1" in recent
        assert "/tmp/project2" in recent
        clear_recent()
        assert get_recent_folders() == []
        reset_config()


class TestCommandDispatchIntegration:
    def test_route_command_file_validation(self):
        from multiformat_validator.commands import route_command
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            json.dump({"key": "value"}, f)
            tmp_path = f.name
        try:
            args = MagicMock()
            args.path = tmp_path
            args.lang = "en"
            args.format = "text"
            args.output = None
            args.recursive = False
            with patch("builtins.input", side_effect=[""]):
                route_command(args)
        finally:
            os.unlink(tmp_path)

    def test_route_command_dir_scan(self):
        from multiformat_validator.commands import route_command
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.json")
            with open(test_file, "w") as f:
                json.dump({"test": True}, f)
            args = MagicMock()
            args.path = tmpdir
            args.lang = "en"
            args.format = "text"
            args.output = None
            args.recursive = False
            route_command(args)

    def test_route_command_dir_with_json_export(self):
        from multiformat_validator.commands import route_command
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.json")
            with open(test_file, "w") as f:
                json.dump({"test": True}, f)
            output_file = os.path.join(tmpdir, "output.json")
            args = MagicMock()
            args.path = tmpdir
            args.lang = "en"
            args.format = "json"
            args.output = output_file
            args.recursive = False
            route_command(args)
            assert os.path.exists(output_file)

    def test_route_command_dir_with_csv_export(self):
        from multiformat_validator.commands import route_command
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.json")
            with open(test_file, "w") as f:
                json.dump({"test": True}, f)
            output_file = os.path.join(tmpdir, "output.csv")
            args = MagicMock()
            args.path = tmpdir
            args.lang = "en"
            args.format = "csv"
            args.output = output_file
            args.recursive = False
            route_command(args)
            assert os.path.exists(output_file)

    def test_route_command_nonexistent_path(self):
        from multiformat_validator.commands import route_command
        args = MagicMock()
        args.path = "/nonexistent/path/that/does/not/exist"
        args.lang = "en"
        args.format = "text"
        args.output = None
        args.recursive = False
        with patch("builtins.print") as mock_print:
            route_command(args)
            assert mock_print.called


class TestCliModeIntegration:
    def test_cli_mode_list_formats(self):
        from multiformat_validator.cli import cli_mode
        args = MagicMock(list_formats=True, lang="en")
        with patch("multiformat_validator.cli.load_config", return_value={"language": "en"}):
            with patch("multiformat_validator.cli.list_formats") as mock_lf:
                cli_mode(args)
                mock_lf.assert_called_once()

    def test_cli_mode_no_path_interactive(self):
        from multiformat_validator.cli import cli_mode
        args = MagicMock(list_formats=False, path=None, lang="en")
        with patch("multiformat_validator.cli.load_config", return_value={"language": "en"}):
            with patch("multiformat_validator.ui.menus.interactive_mode") as mock_im:
                cli_mode(args)
                mock_im.assert_called_once()

    def test_cli_mode_with_path_routes_command(self):
        from multiformat_validator.cli import cli_mode
        args = MagicMock(list_formats=False, path="/some/path", lang="en")
        with patch("multiformat_validator.cli.load_config", return_value={"language": "en"}):
            with patch("multiformat_validator.commands.route_command") as mock_rc:
                cli_mode(args)
                mock_rc.assert_called_once_with(args)

    def test_cli_mode_uses_config_language(self):
        from multiformat_validator.cli import cli_mode
        args = MagicMock(list_formats=True, lang="en")
        with patch("multiformat_validator.cli.load_config", return_value={"language": "zh_CN"}):
            with patch("multiformat_validator.cli.list_formats") as mock_lf:
                cli_mode(args)
                call_args = mock_lf.call_args
                from multiformat_validator.i18n import I18n
                assert isinstance(call_args[0][0], I18n)


class TestFileValidationIntegration:
    def test_validate_valid_json(self):
        from multiformat_validator.commands.validate import _validate_file
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            json.dump({"key": "value"}, f)
            tmp_path = f.name
        try:
            result = _validate_file(tmp_path)
            assert result["valid"] is True
            assert result["errors"] == []
        finally:
            os.unlink(tmp_path)

    def test_validate_invalid_json(self):
        from multiformat_validator.commands.validate import _validate_file
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            f.write("{invalid json")
            tmp_path = f.name
        try:
            result = _validate_file(tmp_path)
            assert result["valid"] is False
            assert len(result["errors"]) > 0
        finally:
            os.unlink(tmp_path)

    def test_validate_nonexistent_file(self):
        from multiformat_validator.commands.validate import _validate_file
        result = _validate_file("/nonexistent/file.json")
        assert result["valid"] is False
        assert result["errors"][0]["type"] == "FileNotFound"

    def test_validate_empty_file(self):
        from multiformat_validator.commands.validate import _validate_file
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            f.write("")
            tmp_path = f.name
        try:
            result = _validate_file(tmp_path)
            assert result["valid"] is False
            assert result["errors"][0]["type"] == "EmptyFile"
        finally:
            os.unlink(tmp_path)

    def test_validate_python_file(self):
        from multiformat_validator.commands.validate import _validate_file
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("def hello():\n    return 'world'\n")
            tmp_path = f.name
        try:
            result = _validate_file(tmp_path)
            assert result["valid"] is True
        finally:
            os.unlink(tmp_path)

    def test_validate_with_ignore_errors(self):
        from multiformat_validator.commands.validate import _validate_file
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            f.write("{invalid json")
            tmp_path = f.name
        try:
            result = _validate_file(tmp_path, ignore_errors=["SyntaxError"])
            assert result["valid"] is False
        finally:
            os.unlink(tmp_path)


class TestI18nIntegration:
    def test_i18n_english(self):
        from multiformat_validator.i18n import I18n
        i18n = I18n("en")
        title = i18n.get("list_formats_title")
        assert title
        assert isinstance(title, str)

    def test_i18n_chinese(self):
        from multiformat_validator.i18n import I18n
        i18n = I18n("zh_CN")
        title = i18n.get("list_formats_title")
        assert title

    def test_i18n_fallback(self):
        from multiformat_validator.i18n import I18n
        i18n = I18n("en")
        result = i18n.get("nonexistent_key_xyz")
        assert result == "nonexistent_key_xyz"


class TestScannerIntegration:
    def test_scan_empty_folder(self):
        from multiformat_validator.scanner import scan_folder
        with tempfile.TemporaryDirectory() as tmpdir:
            results = scan_folder(tmpdir, recursive=False)
            assert results == []

    def test_scan_folder_with_files(self):
        from multiformat_validator.scanner import scan_folder
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "test.json"), "w") as f:
                json.dump({"a": 1}, f)
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write("x = 1\n")
            results = scan_folder(tmpdir, recursive=False)
            assert len(results) == 2
            for r in results:
                assert "file" in r
                assert "valid" in r
                assert "errors" in r

    def test_scan_recursive(self):
        from multiformat_validator.scanner import scan_folder
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, "sub")
            os.makedirs(subdir)
            with open(os.path.join(subdir, "nested.json"), "w") as f:
                json.dump({"nested": True}, f)
            results = scan_folder(tmpdir, recursive=True)
            assert len(results) == 1

    def test_scan_excludes_patterns(self):
        from multiformat_validator.scanner import scan_folder
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "keep.json"), "w") as f:
                json.dump({}, f)
            os.makedirs(os.path.join(tmpdir, "__pycache__"))
            with open(os.path.join(tmpdir, "__pycache__", "cached.json"), "w") as f:
                json.dump({}, f)
            results = scan_folder(tmpdir, recursive=True)
            assert len(results) == 1


class TestExporterIntegration:
    def test_export_json(self):
        from multiformat_validator.exporter import export_json
        results = [{"file": "a.json", "valid": True, "errors": []}]
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            tmp_path = f.name
        try:
            path = export_json(results, tmp_path)
            assert os.path.exists(tmp_path)
            with open(tmp_path) as f:
                data = json.load(f)
            assert "summary" in data
            assert "results" in data
            assert data["summary"]["total"] == 1
            assert data["summary"]["valid"] == 1
            assert len(data["results"]) == 1
        finally:
            os.unlink(tmp_path)

    def test_export_csv(self):
        from multiformat_validator.exporter import export_csv
        results = [{"file": "a.json", "valid": True, "errors": []}]
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            tmp_path = f.name
        try:
            path = export_csv(results, tmp_path)
            assert os.path.exists(tmp_path)
        finally:
            os.unlink(tmp_path)


class TestEncodingIntegration:
    def test_read_utf8(self):
        from multiformat_validator.encoder import read_with_detection
        with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", encoding="utf-8", delete=False) as f:
            f.write("Hello 世界")
            tmp_path = f.name
        try:
            content, encoding = read_with_detection(tmp_path)
            assert "Hello" in content
        finally:
            os.unlink(tmp_path)

    def test_read_nonexistent(self):
        from multiformat_validator.encoder import read_with_detection
        content, encoding = read_with_detection("/nonexistent/file.txt")
        assert content == "" or encoding == "unknown"


class TestHistoryIntegration:
    def test_save_and_get_last_path(self):
        from multiformat_validator.history import save_last_path
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            tmp_path = f.name
        try:
            save_last_path(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_add_record(self):
        from multiformat_validator.history_viewer import add_record
        add_record("/tmp/test.py", True, 0)


class TestDisplayIntegration:
    def test_clear_screen(self):
        from multiformat_validator.display import clear_screen
        clear_screen()

    def test_display_report(self):
        from multiformat_validator.display import display_report
        from multiformat_validator.i18n import I18n
        i18n = I18n("en")
        result = {"valid": True, "errors": []}
        display_report(i18n, result, "/tmp/test.json")
