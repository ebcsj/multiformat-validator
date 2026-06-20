import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestParseArgs:
    def test_no_args(self):
        from multiformat_validator.cli import parse_args
        args = parse_args([])
        assert args.path is None
        assert args.lang == "en"
        assert args.format == "text"
        assert args.output is None
        assert args.recursive is False
        assert args.list_formats is False

    def test_path_arg(self):
        from multiformat_validator.cli import parse_args
        args = parse_args(["myfile.py"])
        assert args.path == "myfile.py"

    def test_lang_flag(self):
        from multiformat_validator.cli import parse_args
        args = parse_args(["-l", "zh_TW"])
        assert args.lang == "zh_TW"

    def test_format_flag(self):
        from multiformat_validator.cli import parse_args
        args = parse_args(["-f", "json"])
        assert args.format == "json"

    def test_output_flag(self):
        from multiformat_validator.cli import parse_args
        args = parse_args(["-o", "report.json"])
        assert args.output == "report.json"

    def test_recursive_flag(self):
        from multiformat_validator.cli import parse_args
        args = parse_args(["-r", "/some/dir"])
        assert args.recursive is True

    def test_list_formats_flag(self):
        from multiformat_validator.cli import parse_args
        args = parse_args(["--list-formats"])
        assert args.list_formats is True

    def test_invalid_lang(self):
        from multiformat_validator.cli import parse_args
        with pytest.raises(SystemExit):
            parse_args(["-l", "fr"])

    def test_invalid_format(self):
        from multiformat_validator.cli import parse_args
        with pytest.raises(SystemExit):
            parse_args(["-f", "xml"])


class TestCleanPath:
    def test_strips_whitespace(self):
        from multiformat_validator.cli import clean_path
        result = clean_path("  /tmp/test  ")
        assert os.path.isabs(result)
        assert result.endswith("test") or result.endswith("tmp")

    def test_removes_double_quotes(self):
        from multiformat_validator.cli import clean_path
        result = clean_path('"/tmp/test"')
        assert os.path.isabs(result)
        assert '"' not in result

    def test_removes_single_quotes(self):
        from multiformat_validator.cli import clean_path
        result = clean_path("'/tmp/test'")
        assert os.path.isabs(result)
        assert "'" not in result

    def test_realpath_normalization(self):
        from multiformat_validator.cli import clean_path
        result = clean_path("/tmp/../tmp/test")
        assert os.path.isabs(result)


class TestListFormats:
    @patch("builtins.print")
    def test_list_formats_prints_output(self, mock_print):
        from multiformat_validator.cli import list_formats
        from multiformat_validator.i18n import I18n
        list_formats(I18n("en"))
        assert mock_print.call_count > 0

    @patch("builtins.print")
    def test_list_formats_default_lang(self, mock_print):
        from multiformat_validator.cli import list_formats
        list_formats(lang="en")
        assert mock_print.call_count > 0


class TestCliMode:
    @patch("multiformat_validator.cli.load_config")
    @patch("multiformat_validator.cli.parse_args")
    def test_list_formats_calls_list_formats(self, mock_parse, mock_config):
        mock_parse.return_value = MagicMock(list_formats=True, lang="en")
        mock_config.return_value = {"language": "en"}
        from multiformat_validator.cli import cli_mode
        with patch("multiformat_validator.cli.list_formats") as mock_lf:
            cli_mode(mock_parse.return_value)
            mock_lf.assert_called_once()

    @patch("multiformat_validator.cli.load_config")
    @patch("multiformat_validator.cli.parse_args")
    def test_no_path_starts_interactive(self, mock_parse, mock_config):
        mock_parse.return_value = MagicMock(list_formats=False, path=None, lang="en")
        mock_config.return_value = {"language": "en"}
        from multiformat_validator.cli import cli_mode
        with patch("multiformat_validator.ui.menus.interactive_mode") as mock_im:
            cli_mode(mock_parse.return_value)
            mock_im.assert_called_once()

    @patch("multiformat_validator.cli.load_config")
    @patch("multiformat_validator.cli.parse_args")
    def test_with_path_routes_command(self, mock_parse, mock_config):
        mock_parse.return_value = MagicMock(list_formats=False, path="/some/path", lang="en")
        mock_config.return_value = {"language": "en"}
        from multiformat_validator.cli import cli_mode
        with patch("multiformat_validator.commands.route_command") as mock_rc:
            cli_mode(mock_parse.return_value)
            mock_rc.assert_called_once_with(mock_parse.return_value)


class TestMain:
    @patch("multiformat_validator.cli.cli_mode")
    @patch("multiformat_validator.cli.parse_args")
    @patch("multiformat_validator.cli.init_config")
    def test_main_calls_init_parse_cli(self, mock_init, mock_parse, mock_cli):
        from multiformat_validator.cli import main
        main()
        mock_init.assert_called_once()
        mock_parse.assert_called_once()
        mock_cli.assert_called_once()


class TestCliEntryPoint:
    def test_cli_imports(self):
        from multiformat_validator.cli import main, parse_args, clean_path, list_formats, cli_mode
        assert callable(main)
        assert callable(parse_args)
        assert callable(clean_path)
        assert callable(list_formats)
        assert callable(cli_mode)

    def test_clean_path_in_cli_module(self):
        from multiformat_validator.cli import clean_path
        result = clean_path('"test.py"')
        assert result.endswith("test.py")
        assert '"' not in result
