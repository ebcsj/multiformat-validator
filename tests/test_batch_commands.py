import pytest
from unittest.mock import patch, MagicMock
from multiformat_validator.commands.batch_scan import run as run_batch_scan
from multiformat_validator.commands.compare import run as run_compare
from multiformat_validator.i18n import I18n


class TestBatchScan:
    @patch("multiformat_validator.commands.batch_scan.display_batch_results")
    @patch("multiformat_validator.commands._scan_folder", return_value=[{"file": "a.json", "valid": True, "errors": []}])
    def test_batch_scan_with_output_file(self, mock_scan, mock_display):
        i18n = I18n("en")
        with patch("builtins.input", side_effect=["/tmp/folder", ""]):
            run_batch_scan(i18n, output_format="json", output_file="report.json")
        assert mock_scan.called
        assert mock_display.called

    @patch("multiformat_validator.commands.batch_scan.display_batch_results")
    @patch("multiformat_validator.commands._scan_folder", return_value=[])
    def test_batch_scan_empty_folder(self, mock_scan, mock_display):
        i18n = I18n("en")
        with patch("builtins.input", side_effect=["/tmp/empty", "", ""]):
            run_batch_scan(i18n)
        assert mock_scan.called
        mock_display.assert_called_once()
        results = mock_display.call_args[0][1]
        assert results == []

    @patch("multiformat_validator.commands.batch_scan.display_batch_results")
    @patch("multiformat_validator.commands._scan_folder", return_value=[
        {"file": "a.json", "valid": True, "errors": []},
        {"file": "b.py", "valid": False, "errors": [{"type": "SyntaxError", "line": 1, "col": 1, "message": "bad"}]},
    ])
    def test_batch_scan_mixed_results(self, mock_scan, mock_display):
        i18n = I18n("en")
        with patch("builtins.input", side_effect=["/tmp/folder", "", ""]):
            run_batch_scan(i18n)
        assert mock_display.called
        results = mock_display.call_args[0][1]
        assert len(results) == 2
        assert results[0]["valid"]
        assert not results[1]["valid"]

    @patch("multiformat_validator.commands.batch_scan.display_batch_results")
    @patch("multiformat_validator.commands._scan_folder", return_value=[{"file": "a.json", "valid": True, "errors": []}])
    def test_batch_scan_export_choice_json(self, mock_scan, mock_display):
        i18n = I18n("en")
        with patch("builtins.input", side_effect=["/tmp/folder", "JSON", "", ""]):
            run_batch_scan(i18n)
        assert mock_scan.called

    @patch("multiformat_validator.commands.batch_scan.display_batch_results")
    @patch("multiformat_validator.commands._scan_folder", return_value=[{"file": "a.json", "valid": True, "errors": []}])
    def test_batch_scan_export_choice_none(self, mock_scan, mock_display):
        i18n = I18n("en")
        with patch("builtins.input", side_effect=["/tmp/folder", "", "", ""]):
            run_batch_scan(i18n)
        assert mock_scan.called


class TestCompare:
    @patch("multiformat_validator.commands.compare._validate_file")
    def test_compare_same_files(self, mock_validate):
        i18n = I18n("en")
        mock_validate.return_value = {"valid": True, "errors": []}
        with patch("builtins.input", side_effect=["a.json", "b.json", ""]):
            run_compare(i18n)
        assert mock_validate.call_count == 2

    @patch("multiformat_validator.commands.compare._validate_file")
    def test_compare_different_files(self, mock_validate):
        i18n = I18n("en")
        mock_validate.side_effect = [
            {"valid": True, "errors": []},
            {"valid": False, "errors": [{"type": "SyntaxError", "line": 1, "col": 1, "message": "bad"}]},
        ]
        with patch("builtins.input", side_effect=["a.json", "b.json", ""]):
            run_compare(i18n)
        assert mock_validate.call_count == 2

    @patch("multiformat_validator.commands.compare._validate_file")
    def test_compare_nonexistent_files(self, mock_validate):
        i18n = I18n("en")
        mock_validate.return_value = {"valid": False, "errors": [{"type": "FileNotFound", "line": 0, "col": 0, "message": "not found"}]}
        with patch("builtins.input", side_effect=["nonexistent1.txt", "nonexistent2.txt", ""]):
            run_compare(i18n)
        assert mock_validate.call_count == 2

    @patch("multiformat_validator.commands.compare._validate_file")
    def test_compare_both_invalid_same_errors(self, mock_validate):
        i18n = I18n("en")
        error = {"type": "EmptyFile", "line": 0, "col": 0, "message": "empty"}
        mock_validate.return_value = {"valid": False, "errors": [error]}
        with patch("builtins.input", side_effect=["a.txt", "b.txt", ""]):
            run_compare(i18n)
        assert mock_validate.call_count == 2

    @patch("multiformat_validator.commands.compare._validate_file")
    def test_compare_with_config_ignore(self, mock_validate):
        i18n = I18n("en")
        config = {"ignore_errors": ["EmptyFile"]}
        mock_validate.return_value = {"valid": True, "errors": []}
        with patch("builtins.input", side_effect=["a.json", "b.json", ""]):
            run_compare(i18n, config=config)
        assert mock_validate.call_count == 2
        for call_args in mock_validate.call_args_list:
            assert call_args[0][1] == ["EmptyFile"]
