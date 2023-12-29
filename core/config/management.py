from argparse import Namespace
from typing import Any

from core.config.parser import ArgConfigParser
from core.config.parser import IniConfigParser
import core.paths

c_paths = core.paths.Paths()


class ConfigManager:
    """
    Helper class to handle configuration from several
    locations (arguments, file)
    """
    CONF_FILE_PARAM = 'config_file'

    config_defaults: dict = {
        'origin': 'https://github.com/worstprgr/git-observer/commit/',
        'filepath': c_paths.BASE_DIR,
        'logfolders': ['.'],
        'ignore': [],
        'show_viewer': False,
        'descending': False
    }

    __active_config__: Namespace = None

    @staticmethod
    def get_app_config() -> Namespace:
        """
        Loads the config from known locations and merges it
        with default config to be returned
        :return: (default) config as Namespace
        """
        if ConfigManager.__active_config__:
            return ConfigManager.__active_config__

        config = ConfigManager.__get_plain_config__()
        if config is None:
            return ConfigManager.get_defaults()

        config_merge = ConfigManager.get_defaults()
        for key in config_merge.__dict__.keys():
            if key in config:
                config_merge.__dict__[key] = config.__dict__[key]

        ConfigManager.__active_config__ = config_merge
        return ConfigManager.__active_config__

    @staticmethod
    def __get_plain_config__() -> Namespace | None:
        """
        Loads the config in order args, file and returns it
        :return: config as Namespace. DEFAULT: None
        """
        arg_parser = ArgConfigParser(ConfigManager.config_defaults)
        # If there are arguments these are preferred over file
        if arg_parser.has_config():
            arg_config = arg_parser.parse_config()
            # If arguments reference a config file this one will be used
            if ConfigManager.CONF_FILE_PARAM in arg_config:
                file_parser = IniConfigParser(ConfigManager.config_defaults, arg_config.config_file)
                # Check, if config file provided by argument reference even exists
                if file_parser.has_config():
                    return file_parser.parse_config()
            # Return argument config if file not given or failed
            return arg_config

        # If no arguments are given, we check for INI file
        file_parser = IniConfigParser(ConfigManager.config_defaults)
        if file_parser.has_config():
            return file_parser.parse_config()

        return None

    @staticmethod
    def get_defaults() -> Namespace:
        """
        Method to determine if implemented parser can provide
        a valid user configuration
        :return: TRUE when parser can be used as configuration source
        """
        config_result = Namespace()
        for key in ConfigManager.config_defaults.keys():
            config_result.__dict__[key] = ConfigManager.config_defaults[key]
        return config_result

    def __init__(self):
        self.active_config = ConfigManager.__active_config__
        self.simplified_config = self.get_simplified_config()
        self.persistent_handler = IniConfigParser(default_config=self.simplified_config)

    def get_simplified_config(self) -> dict:
        """
        Returns a dictionary that represents current config
        using human-readable and native data types str and bool
        """
        result: dict[str, Any] = dict()
        for key in self.active_config.__dict__.keys():
            current_val = self.active_config.__dict__.get(key)
            value: Any
            if type(current_val) is list:
                value = str.join(', ', current_val)
            else:
                value = current_val
            result[key] = value
        return result

    def apply_changes(self, edit_values: dict):
        """
        If changed, the parameter edit_values will be
        applied to persistent (default) file
        :param: edit_value changed config to be stored to file
        """
        if not self.has_changes(edit_values):
            return

        save_values: dict = dict()
        for key in edit_values.keys():
            value = edit_values[key]
            if type(self.active_config.__dict__[key]) is list:
                value = [x.strip() for x in value.split(',')]
            save_values[key] = value

        self.persistent_handler.persist_config(save_values)

    def has_changes(self, edit_values: dict) -> bool:
        """
        Checks if given config has changed in comparison with
        current instance active config
        """
        for key in self.simplified_config.keys():
            value_old = self.simplified_config.get(key)
            value_current = edit_values.get(key)
            if not (value_old == value_current):
                return True
        return False
