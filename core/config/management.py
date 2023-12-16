from argparse import Namespace

from core.config.parser import ArgConfigParser
from core.config.parser import IniConfigParser
import core.paths as c_paths


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

    @staticmethod
    def get_config() -> Namespace:
        """
        Loads the config from known locations and merges it
        with default config to be returned
        :return: (default) config as Namespace
        """
        config = ConfigManager.__get_plain_config__()
        if config is None:
            return ConfigManager.get_defaults()

        config_merge = ConfigManager.get_defaults()
        for key in config_merge.__dict__.keys():
            if key in config:
                config_merge.__dict__[key] = config.__dict__[key]
        return config_merge

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
