import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from multiformat_validator.i18n import I18n


def _mock_config():
    return {"language": "en", "theme": "dark", "output_format": "text", "ignore_errors": [], "logging_enabled": False}


class TestSettingsMenu:
    @patch("multiformat_validator.display.clear_screen")
    @patch("builtins.input", return_value="0")
    def test_exit_returns_immediately(self, mock_input, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        i18n = I18n("en")
        config = _mock_config()
        result_i18n, result_config = settings_menu(i18n, config)
        assert result_config == config

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings.change_language")
    @patch("builtins.input", side_effect=["1", "0"])
    def test_change_language_dispatch(self, mock_input, mock_cl, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        mock_cl.return_value = (I18n("en"), _mock_config())
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_cl.assert_called_once_with(config)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings.change_output_format")
    @patch("builtins.input", side_effect=["2", "0"])
    def test_change_output_format_dispatch(self, mock_input, mock_cf, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        mock_cf.return_value = _mock_config()
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_cf.assert_called_once_with(config)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings.change_theme")
    @patch("builtins.input", side_effect=["3", "0"])
    def test_change_theme_dispatch(self, mock_input, mock_ct, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        mock_ct.return_value = _mock_config()
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_ct.assert_called_once_with(config)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings.manage_ignore_errors")
    @patch("builtins.input", side_effect=["5", "0"])
    def test_manage_ignore_errors_dispatch(self, mock_input, mock_ie, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        mock_ie.return_value = _mock_config()
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_ie.assert_called_once_with(i18n, config)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings.manage_plugins")
    @patch("builtins.input", side_effect=["6", "0"])
    def test_manage_plugins_dispatch(self, mock_input, mock_mp, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_mp.assert_called_once_with(i18n)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings.toggle_logging")
    @patch("builtins.input", side_effect=["7", "0"])
    def test_toggle_logging_dispatch(self, mock_input, mock_tl, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        mock_tl.return_value = _mock_config()
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_tl.assert_called_once_with(i18n, config)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings.check_for_updates")
    @patch("builtins.input", side_effect=["8", "0"])
    def test_check_for_updates_dispatch(self, mock_input, mock_cu, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_cu.assert_called_once_with(i18n, config)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings.show_version_info")
    @patch("builtins.input", side_effect=["9", "0"])
    def test_show_version_info_dispatch(self, mock_input, mock_vi, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_vi.assert_called_once_with(i18n)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings.manage_config")
    @patch("builtins.input", side_effect=["C", "0"])
    def test_manage_config_dispatch(self, mock_input, mock_mc, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        mock_mc.return_value = _mock_config()
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_mc.assert_called_once_with(i18n, config)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.history.clear_history")
    @patch("builtins.input", side_effect=["4", "", "0"])
    def test_clear_history_dispatch(self, mock_input, mock_clear_hist, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        i18n = I18n("en")
        config = _mock_config()
        settings_menu(i18n, config)
        mock_clear_hist.assert_called_once()

    @patch("multiformat_validator.display.clear_screen")
    @patch("builtins.input", side_effect=["Z", "0"])
    def test_invalid_choice_loops(self, mock_input, mock_clear):
        from multiformat_validator.config.settings import settings_menu
        i18n = I18n("en")
        config = _mock_config()
        result_i18n, result_config = settings_menu(i18n, config)
        assert result_config == config


class TestChangeLanguage:
    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings._get_config_module")
    @patch("builtins.input", return_value="3")
    def test_change_to_english(self, mock_input, mock_cfg_fn, mock_clear):
        from multiformat_validator.config.settings import change_language
        mock_cfg = MagicMock()
        mock_cfg_fn.return_value = mock_cfg
        config = _mock_config()
        result_i18n, result_config = change_language(config)
        assert result_config["language"] == "en"
        mock_cfg.save_config.assert_called_once()

    @patch("multiformat_validator.display.clear_screen")
    @patch("builtins.input", return_value="99")
    def test_invalid_choice_returns_original(self, mock_input, mock_clear):
        from multiformat_validator.config.settings import change_language
        config = _mock_config()
        result_i18n, result_config = change_language(config)
        assert result_config == config


class TestChangeOutputFormat:
    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings._get_config_module")
    @patch("builtins.input", return_value="2")
    def test_change_to_json(self, mock_input, mock_cfg_fn, mock_clear):
        from multiformat_validator.config.settings import change_output_format
        mock_cfg = MagicMock()
        mock_cfg_fn.return_value = mock_cfg
        config = _mock_config()
        result = change_output_format(config)
        assert result["output_format"] == "json"

    @patch("multiformat_validator.display.clear_screen")
    @patch("builtins.input", return_value="99")
    def test_invalid_choice_returns_original(self, mock_input, mock_clear):
        from multiformat_validator.config.settings import change_output_format
        config = _mock_config()
        result = change_output_format(config)
        assert result == config


class TestChangeTheme:
    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings._get_config_module")
    @patch("builtins.input", return_value="2")
    def test_change_to_light(self, mock_input, mock_cfg_fn, mock_clear):
        from multiformat_validator.config.settings import change_theme
        mock_cfg = MagicMock()
        mock_cfg_fn.return_value = mock_cfg
        config = _mock_config()
        result = change_theme(config)
        assert result["theme"] == "light"

    @patch("multiformat_validator.display.clear_screen")
    @patch("builtins.input", return_value="99")
    def test_invalid_choice_returns_original(self, mock_input, mock_clear):
        from multiformat_validator.config.settings import change_theme
        config = _mock_config()
        result = change_theme(config)
        assert result == config


class TestManageIgnoreErrors:
    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings._get_config_module")
    @patch("builtins.input", side_effect=["MissingSemicolon,TrailingComma", ""])
    def test_sets_ignore_errors(self, mock_input, mock_cfg_fn, mock_clear):
        from multiformat_validator.config.settings import manage_ignore_errors
        mock_cfg = MagicMock()
        mock_cfg_fn.return_value = mock_cfg
        i18n = I18n("en")
        config = _mock_config()
        result = manage_ignore_errors(i18n, config)
        assert result["ignore_errors"] == ["MissingSemicolon", "TrailingComma"]

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings._get_config_module")
    @patch("builtins.input", side_effect=["", ""])
    def test_empty_input_clears_ignore_errors(self, mock_input, mock_cfg_fn, mock_clear):
        from multiformat_validator.config.settings import manage_ignore_errors
        mock_cfg = MagicMock()
        mock_cfg_fn.return_value = mock_cfg
        i18n = I18n("en")
        config = _mock_config()
        config["ignore_errors"] = ["OldError"]
        result = manage_ignore_errors(i18n, config)
        assert result["ignore_errors"] == []


class TestToggleLogging:
    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings._get_config_module")
    @patch("builtins.input", side_effect=["1", ""])
    def test_enable_logging(self, mock_input, mock_cfg_fn, mock_clear):
        from multiformat_validator.config.settings import toggle_logging
        mock_cfg = MagicMock()
        mock_cfg_fn.return_value = mock_cfg
        i18n = I18n("en")
        config = _mock_config()
        result = toggle_logging(i18n, config)
        assert result["logging_enabled"] is True

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.config.settings._get_config_module")
    @patch("builtins.input", side_effect=["2", ""])
    def test_disable_logging(self, mock_input, mock_cfg_fn, mock_clear):
        from multiformat_validator.config.settings import toggle_logging
        mock_cfg = MagicMock()
        mock_cfg_fn.return_value = mock_cfg
        i18n = I18n("en")
        config = _mock_config()
        config["logging_enabled"] = True
        result = toggle_logging(i18n, config)
        assert result["logging_enabled"] is False

    @patch("multiformat_validator.display.clear_screen")
    @patch("builtins.input", side_effect=["0", ""])
    def test_back_does_not_change(self, mock_input, mock_clear):
        from multiformat_validator.config.settings import toggle_logging
        i18n = I18n("en")
        config = _mock_config()
        result = toggle_logging(i18n, config)
        assert result["logging_enabled"] is False


class TestManageTemplates:
    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.templates.list_templates", return_value=[])
    @patch("builtins.input", return_value="0")
    def test_exit_returns_config(self, mock_input, mock_list, mock_clear):
        from multiformat_validator.config.templates import manage_templates
        i18n = I18n("en")
        config = _mock_config()
        result = manage_templates(i18n, config)
        assert result == config

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.templates.list_templates", return_value=[])
    @patch("builtins.input", return_value="0")
    def test_lists_no_templates(self, mock_input, mock_list, mock_clear):
        from multiformat_validator.config.templates import manage_templates
        i18n = I18n("en")
        config = _mock_config()
        manage_templates(i18n, config)
        mock_list.assert_called_once()

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.templates.save_template")
    @patch("multiformat_validator.templates.list_templates", return_value=[])
    @patch("builtins.input", side_effect=["1", "my_template", "", "0"])
    def test_save_template(self, mock_input, mock_list, mock_save, mock_clear):
        from multiformat_validator.config.templates import manage_templates
        i18n = I18n("en")
        config = _mock_config()
        manage_templates(i18n, config)
        mock_save.assert_called_once_with("my_template", config)

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.templates.list_templates", return_value=["existing"])
    @patch("multiformat_validator.templates.load_template", return_value={"theme": "light"})
    @patch("builtins.input", side_effect=["2", "existing", "", "0"])
    def test_load_template(self, mock_input, mock_load, mock_list, mock_clear):
        from multiformat_validator.config.templates import manage_templates
        i18n = I18n("en")
        config = _mock_config()
        result = manage_templates(i18n, config)
        mock_load.assert_called_once_with("existing")
        assert result["theme"] == "light"

    @patch("multiformat_validator.display.clear_screen")
    @patch("multiformat_validator.templates.list_templates", return_value=["old_template"])
    @patch("multiformat_validator.templates.delete_template", return_value=True)
    @patch("builtins.input", side_effect=["3", "old_template", "", "0"])
    def test_delete_template(self, mock_input, mock_delete, mock_list, mock_clear):
        from multiformat_validator.config.templates import manage_templates
        i18n = I18n("en")
        config = _mock_config()
        manage_templates(i18n, config)
        mock_delete.assert_called_once_with("old_template")


class TestModuleExports:
    def test_settings_module_importable(self):
        from multiformat_validator.config.settings import settings_menu
        assert callable(settings_menu)

    def test_templates_module_importable(self):
        from multiformat_validator.config.templates import manage_templates
        assert callable(manage_templates)

    def test_all_new_functions_importable(self):
        from multiformat_validator.config import (
            settings_menu, change_language, change_output_format, change_theme,
            manage_ignore_errors, toggle_logging, manage_config,
            check_for_updates, show_version_info, manage_plugins,
            manage_templates,
        )
        for fn in [settings_menu, change_language, change_output_format, change_theme,
                   manage_ignore_errors, toggle_logging, manage_config,
                   check_for_updates, show_version_info, manage_plugins,
                   manage_templates]:
            assert callable(fn)

    def test_config_base_functions_still_importable(self):
        from multiformat_validator.config import (
            load_config, save_config, init_config,
            add_recent_file, add_recent_folder,
        )
        assert callable(load_config)
        assert callable(save_config)
        assert callable(init_config)
        assert callable(add_recent_file)
        assert callable(add_recent_folder)
