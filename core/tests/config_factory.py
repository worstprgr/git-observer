from argparse import Namespace
from core.config import ConfigHandler


class ConfigFactory:
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
