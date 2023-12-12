#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from argparse import Namespace
from pathlib import Path

import core.paths as c_paths
from configparser import ConfigParser


def parse_value(value: str, default_val):
    """
    Basically a string parser converting a string value
    to list, bool, int or string
    :param value:
    :param default_val:
    :return:
    """
    if type(default_val) is list:
        return [item.strip() for item in value.split(',')]
    if type(default_val) is bool:
        return bool(value)
    if type(default_val) is int:
        return int(value)
    return value


class ConfigHandler:
    """
    Helper class to handle configuration from several
    locations (arguments, file)
    """

    config_names_ini_defaults: dict = {
        'origin': 'https://github.com/worstprgr/git-observer/commit/',
        'filepath': c_paths.BASE_DIR,
        'logfolders': ['.'],
        'ignore': [],
        'show_viewer': True,
        'descending': True
    }

    config_name_defaults: dict = {
        'origin': 'https://github.com/worstprgr/git-observer/commit/',
        'filepath': c_paths.BASE_DIR,
        'logfolders': ['.'],
        'ignore': [],
        'show_viewer': False,
        'descending': False
    }

    def __init__(self):
        self.config_ini_file: str = c_paths.CONFIG_INI

    def config_exists(self):
        ini_file = Path(self.config_ini_file)
        return ini_file.is_file()

    def install(self):
        """
        If not present, the default configuration is
        stored in local config.ini file
        :return:
        """
        if self.config_exists():
            return

        config = ConfigParser()
        config.add_section('Default')
        for key in self.config_names_ini_defaults.keys():
            value = self.config_names_ini_defaults[key]
            if type(value) is list:
                config['Default'][key] = str.join(', ', value)
            else:
                config['Default'][key] = str(value)

        with open(self.config_ini_file, 'w') as ini:
            config.write(ini)

    # TODO @worstprgr: Separate the parser from the config builder logic, so we can test the argparse directly.
    #       Like in: https://stackoverflow.com/a/18161115/14659310
    def parse_arguments(self) -> Namespace:
        """
        Parses the given arguments passed by caller and
        returns the parsed result
        :return: Namespace hilding the config parameters
        """
        parser = ArgumentParser(allow_abbrev=True)
        parser.add_argument('-o', '--origin', metavar='origin',
                            default='https://github.com/worstprgr/git-observer/commit/',  # Default to repo at GitHub
                            help='Origin path to build commit link for output', required=False)
        parser.add_argument('-fp', '--filepath', action='store', default=c_paths.BASE_DIR,
                            help='Git root to be observed', required=False)
        parser.add_argument('-lf', '--logfolders', metavar='Folder', type=str, nargs='+',
                            default='.', help='Folder(s) to be observed', required=False)
        parser.add_argument('-ig', '--ignore', metavar='Author', type=str, nargs='+',
                            help='Author name to be ignored')
        parser.add_argument('-ui', '--show-viewer', action='store_true', default=False,
                            help='Flag to determine if application should open a grid in UI')
        parser.add_argument('-desc', '--descending', action='store_true', default=False,
                            help='Flag if output should be descending. DEFAULT for --use-viewer')
        parser.add_argument('-cnf', '--config-file', action='store', default=None,
                            help='Configuration file to receive application config from')

        arg_obj = parser.parse_args()
        if arg_obj.config_file:
            return self.handle_file_argument(arg_obj)

        args = vars(arg_obj)
        config_result = Namespace()
        for key in self.config_name_defaults.keys():
            arg_value = args.get(key)
            def_value = self.config_names_ini_defaults[key]
            if arg_value:
                config_result.__dict__[key] = parse_value(arg_value, def_value)
            else:
                config_result.__dict__[key] = def_value
        return config_result

    def handle_file_argument(self, file_name) -> Namespace:
        """
        Handles given file as configuration file
        or returns default fallback
        :param file_name:
        :return:
        """
        self.config_ini_file = file_name.config_file
        if self.config_exists():
            return self.parse_config_file()
        else:
            return self.no_args_fallback()

    def parse_config_file(self) -> Namespace:
        """
        Parses configuration INI file associated with this
        instance
        :return: Namespace holding the config parameters
        """
        parser = ConfigParser()
        parser.read(self.config_ini_file)
        if 'Default' not in parser.sections():
            raise RuntimeError('Invalid config file given')

        config_result = Namespace()
        for key in self.config_names_ini_defaults.keys():
            def_value = self.config_names_ini_defaults[key]
            arg_value = None
            if key in parser['Default']:
                arg_value = parser['Default'][key]

            if arg_value:
                config_result.__dict__[key] = parse_value(arg_value, def_value)
            else:
                config_result.__dict__[key] = self.config_names_ini_defaults[key]
        return config_result

    def no_args_fallback(self) -> Namespace:
        """
        Fallback method for invalid or no arguments passed
        :return:
        """
        # Install when doesn't exist
        if not self.config_exists():
            self.install()
        return self.parse_config_file()

    @staticmethod
    def get_app_config() -> Namespace:
        """
        Gets the configuration for application runtime in multiple steps:\n
        * When no arguments are given\n
        \t* May create default configuration file if not exists\n
        \t* Use (new) configuration file\n
        * Arguments given\n
        \t* Configuration file from arguments\n
        \t* Arguments itself
        :return: Namespace holding config
        """
        config_handler = ConfigHandler()
        if len(sys.argv) <= 1:
            return config_handler.no_args_fallback()

        return config_handler.parse_arguments()
