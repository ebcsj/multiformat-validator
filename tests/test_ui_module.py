import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from multiformat_validator.i18n import I18n
from multiformat_validator.ui.prompts import clean_path
from multiformat_validator.commands.export import run as run_export


class TestCleanPath:
    def test_strips_whitespace(self):
        result = clean_path("  /tmp/test  ")
        assert os.path.isabs(result)
        assert result.endswith("tmp") or result.endswith("test")

    def test_removes_double_quotes(self):
        result = clean_path('"/tmp/test"')
        assert os.path.isabs(result)
        assert "tmp" in result and "test" in result

    def test_removes_single_quotes(self):
        result = clean_path("'/tmp/test'")
        assert os.path.isabs(result)
        assert "tmp" in result and "test" in result

    def test_preserves_unquoted_path(self):
        result = clean_path("/tmp/test")
        assert os.path.isabs(result)
        assert "tmp" in result and "test" in result

    def test_realpath_normalization(self):
        result = clean_path("/tmp/../tmp/test")
        assert os.path.isabs(result)
        assert "tmp" in result and "test" in result

    def test_no_quotes_in_result(self):
        result = clean_path('"some/path"')
        assert '"' not in result
        assert "'" not in result

    def test_strips_only_surrounding_quotes(self):
        result = clean_path("a\"b'c")
        assert "a\"b'c" in result


class TestExportCommand:
    @patch("multiformat_validator.commands._scan_folder")
    @patch("multiformat_validator.commands.export.export_json")
    def test_batch_export_json(self, mock_export_json, mock_scan):
        mock_scan.return_value = [{"file": "a.json", "valid": True, "errors": []}]
        mock_export_json.return_value = "batch_report.json"
        i18n = I18n("en")
        with patch("builtins.input", side_effect=["/tmp/folder", "JSON", "report.json", ""]):
            run_export(i18n)
        mock_scan.assert_called_once()
        mock_export_json.assert_called_once()

    @patch("multiformat_validator.commands._scan_folder")
    @patch("multiformat_validator.commands.export.export_csv")
    def test_batch_export_csv(self, mock_export_csv, mock_scan):
        mock_scan.return_value = [{"file": "a.json", "valid": True, "errors": []}]
        mock_export_csv.return_value = "batch_report.csv"
        i18n = I18n("en")
        with patch("builtins.input", side_effect=["/tmp/folder", "CSV", "report.csv", ""]):
            run_export(i18n)
        mock_scan.assert_called_once()
        mock_export_csv.assert_called_once()

    @patch("multiformat_validator.commands._scan_folder")
    @patch("multiformat_validator.commands.export.export_json")
    def test_batch_export_defaults_to_json(self, mock_export_json, mock_scan):
        mock_scan.return_value = []
        mock_export_json.return_value = "batch_report.json"
        i18n = I18n("en")
        with patch("builtins.input", side_effect=["/tmp/folder", "invalid", "", ""]):
            run_export(i18n)
        mock_export_json.assert_called_once()

    @patch("multiformat_validator.commands._scan_folder")
    @patch("multiformat_validator.commands.export.export_json")
    def test_batch_export_default_output_name(self, mock_export_json, mock_scan):
        mock_scan.return_value = []
        mock_export_json.return_value = "batch_report.json"
        i18n = I18n("en")
        with patch("builtins.input", side_effect=["/tmp/folder", "JSON", "", ""]):
            run_export(i18n)
        args = mock_export_json.call_args[0]
        assert args[1] == "batch_report.json"


class TestInteractiveMode:
    def _get_mock_config(self):
        return {"language": "en", "theme": "dark", "output_format": "text"}

    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["X"])
    def test_interactive_mode_exit(self, mock_input, mock_last_path, mock_clear):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit) as mock_exit:
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
            mock_exit.assert_called_once_with(0)

    @patch("multiformat_validator.ui.menus.show_help")
    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["H", "X"])
    def test_interactive_mode_help(self, mock_input, mock_last_path, mock_clear, mock_help):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_help.assert_called_once()

    @patch("multiformat_validator.ui.menus.show_stats")
    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["7", "X"])
    def test_interactive_mode_stats(self, mock_input, mock_last_path, mock_clear, mock_stats):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_stats.assert_called_once()

    @patch("multiformat_validator.ui.menus.show_history")
    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["8", "X"])
    def test_interactive_mode_history(self, mock_input, mock_last_path, mock_clear, mock_history):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_history.assert_called_once()

    @patch("multiformat_validator.ui.menus.manage_rules")
    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["R", "X"])
    def test_interactive_mode_rules(self, mock_input, mock_last_path, mock_clear, mock_rules):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_rules.assert_called_once()

    @patch("multiformat_validator.ui.menus.manage_plugins")
    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["P", "X"])
    def test_interactive_mode_plugins(self, mock_input, mock_last_path, mock_clear, mock_plugins):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_plugins.assert_called_once()

    @patch("multiformat_validator.ui.menus.manage_quick_validate")
    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["Q", "X"])
    def test_interactive_mode_quick_validate(self, mock_input, mock_last_path, mock_clear, mock_qv):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_qv.assert_called_once()

    @patch("multiformat_validator.ui.menus.manage_custom_validators")
    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["9", "X"])
    def test_interactive_mode_custom_validators(self, mock_input, mock_last_path, mock_clear, mock_cv):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_cv.assert_called_once()

    @patch("multiformat_validator.ui.menus.manage_templates")
    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["6", "X"])
    def test_interactive_mode_templates(self, mock_input, mock_last_path, mock_clear, mock_tmpl):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_tmpl.assert_called_once()

    @patch("multiformat_validator.ui.menus.settings_menu")
    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["S", "X"])
    def test_interactive_mode_settings(self, mock_input, mock_last_path, mock_clear, mock_settings):
        i18n = I18n("en")
        config = self._get_mock_config()
        mock_settings.return_value = (i18n, config)
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_settings.assert_called_once()

    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value="/last/file.py")
    @patch("multiformat_validator.commands.validate.run")
    @patch("builtins.input", side_effect=["0", "X"])
    def test_interactive_mode_retry(self, mock_input, mock_validate, mock_last_path, mock_clear):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)
        mock_validate.assert_called_once()

    @patch("multiformat_validator.ui.menus.clear_screen")
    @patch("multiformat_validator.ui.menus.get_last_path", return_value=None)
    @patch("builtins.input", side_effect=["", "X"])
    def test_interactive_mode_empty_input(self, mock_input, mock_last_path, mock_clear):
        i18n = I18n("en")
        config = self._get_mock_config()
        from multiformat_validator.ui.menus import interactive_mode
        with patch.object(sys, "exit", side_effect=SystemExit):
            with pytest.raises(SystemExit):
                interactive_mode(i18n, config)


class TestMenusModuleExports:
    def test_interactive_mode_importable(self):
        from multiformat_validator.ui import interactive_mode
        assert callable(interactive_mode)

    def test_clean_path_importable_from_prompts(self):
        from multiformat_validator.ui.prompts import clean_path
        assert callable(clean_path)

    def test_clean_path_importable_from_ui(self):
        from multiformat_validator.ui import clean_path
        assert callable(clean_path)

    def test_export_module_importable(self):
        from multiformat_validator.commands.export import run
        assert callable(run)

    def test_ui_init_exports(self):
        from multiformat_validator.ui import interactive_mode, clean_path
        assert interactive_mode is not None
        assert clean_path is not None
