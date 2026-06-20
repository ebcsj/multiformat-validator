from .settings import (
    settings_menu, change_language, change_output_format, change_theme,
    manage_ignore_errors, toggle_logging, manage_config,
    check_for_updates, show_version_info, manage_plugins,
)
from .templates import manage_templates

import importlib.util
import os

_config_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")
_spec = importlib.util.spec_from_file_location("_config_original", _config_py_path)
_config_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_config_module)

load_config = _config_module.load_config
save_config = _config_module.save_config
reset_config = _config_module.reset_config
backup_config = _config_module.backup_config
restore_config = _config_module.restore_config
list_backups = _config_module.list_backups
export_config = _config_module.export_config
import_config = _config_module.import_config
add_recent_file = _config_module.add_recent_file
add_recent_folder = _config_module.add_recent_folder
get_recent_files = _config_module.get_recent_files
get_recent_folders = _config_module.get_recent_folders
clear_recent = _config_module.clear_recent
get_config_path = _config_module.get_config_path
init_config = _config_module.init_config
CONFIG_DIR = _config_module.CONFIG_DIR
CONFIG_FILE = _config_module.CONFIG_FILE
BACKUP_DIR = _config_module.BACKUP_DIR
DEFAULT_CONFIG = _config_module.DEFAULT_CONFIG

__all__ = [
    'settings_menu', 'change_language', 'change_output_format', 'change_theme',
    'manage_ignore_errors', 'toggle_logging', 'manage_config',
    'check_for_updates', 'show_version_info', 'manage_plugins',
    'manage_templates',
    'load_config', 'save_config', 'reset_config', 'backup_config', 'restore_config',
    'list_backups', 'export_config', 'import_config', 'add_recent_file', 'add_recent_folder',
    'get_recent_files', 'get_recent_folders', 'clear_recent', 'get_config_path', 'init_config',
    'CONFIG_DIR', 'CONFIG_FILE', 'BACKUP_DIR', 'DEFAULT_CONFIG',
]
