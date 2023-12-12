import pathlib
from configparser import ConfigParser
from argparse import Namespace

from core.config import ConfigHandler
import core.paths as c_paths


class ConfigFactory:
    # Static object, for comparing keywords inside a namespace
    test_keywords = [
        '[Default]',
        'origin',
        'filepath',
        'logfolders',
        'ignore',
        'show_viewer',
        'descending'
    ]

    config_names_ini_defaults: dict = {
        'origin': 'https://github.com/worstprgr/git-observer/commit/',
        'filepath': c_paths.BASE_DIR,
        'logfolders': ['.'],
        'ignore': [],
        'show_viewer': True,
        'descending': True
    }

    @staticmethod
    def create_defaults():
        """
        Creates a Namespace container
        that represents default configuration for GitObserver
        :return: default config
        """
        namespace = Namespace()
        for key in ConfigHandler.config_name_defaults.keys():
            namespace.__dict__[key] = ConfigHandler.config_name_defaults[key]
        return namespace

    def create_config_file(self, fp: str | pathlib.Path):
        """
        Installing a config file
        """
        config = ConfigParser()
        config.add_section('Default')
        for key in self.config_names_ini_defaults.keys():
            value = self.config_names_ini_defaults[key]
            if type(value) is list:
                config['Default'][key] = str.join(', ', value)
            else:
                config['Default'][key] = str(value)

        with open(fp, 'w') as ini:
            config.write(ini)
