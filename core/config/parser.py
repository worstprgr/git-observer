from argparse import Namespace, ArgumentParser, Action
from configparser import ConfigParser

import core.paths
from core.utils import TypeUtil, PathUtils


c_paths = core.paths.Paths()


class ConfigSourceParser:
    """
    Interface for configuration parsers
    having different sources
    """

    def __init__(self, default_config: dict):
        self.default_config = default_config

    def parse_config(self) -> Namespace:
        """
        Method to parse a config from source
        implemented by inheritance
        :return: Namespace representing our configuration
        """
        raise NotImplementedError('Needs to be overridden')

    def has_config(self) -> bool:
        """
        Method to determine if implemented parser can provide
        a valid user configuration
        :return: TRUE when parser can be used as configuration source
        """
        raise NotImplementedError('Needs to be overridden')


class IniConfigParser(ConfigSourceParser):
    """
    ConfigSourceParser implementation that parses
    its configuration based on *.ini files
    """

    def __init__(self, default_config: dict, config_file: str = c_paths.CONFIG_INI):
        super().__init__(default_config)
        self.config_ini_file: str = config_file

    def has_config(self) -> bool:
        ini_file = PathUtils.conv_to_path_object(self.config_ini_file)
        return ini_file.is_file()

    def parse_config(self) -> Namespace:
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
        for key in parser['Default'].keys():
            def_value = self.default_config[key]
            file_value = None
            if key in parser['Default']:
                file_value = parser['Default'][key]

            if file_value:
                config_result.__dict__[key] = TypeUtil.parse_value(file_value, def_value)
        return config_result

    def install(self):
        """
        If not present, the default configuration is
        stored in local config.ini file
        :return:
        """
        if self.has_config():
            return

        config = ConfigParser()
        config.add_section('Default')
        for key in self.default_config.keys():
            value = self.default_config[key]
            if type(value) is list:
                config['Default'][key] = str.join(', ', value)
            else:
                config['Default'][key] = str(value)
        config['Default'].show_viewer = True
        config['Default'].descending = True
        with open(self.config_ini_file, 'w') as ini:
            config.write(ini)


class ArgConfigParser(ConfigSourceParser):
    """
    ConfigSourceParser implementation that parses
    its configuration based on given shell arguments
    """

    def __init__(self, default_config: dict, ):
        super().__init__(default_config)
        self.registered_args: list[str] = []

    def parse_config(self) -> Namespace:
        """
        Parses the given arguments passed by caller and
        returns the parsed result
        :return: Namespace hilding the config parameters
        """
        parser = self.build_parser()

        arg_obj = parser.parse_args()
        args = vars(arg_obj)
        config_result = Namespace()
        for key in args.keys():
            def_value = None
            if key in self.default_config:
                def_value = self.default_config[key]
            arg_value = None
            if key in args and not (args[key] is None):
                arg_value = args[key]

            if arg_value:
                config_result.__dict__[key] = TypeUtil.parse_value(arg_value, def_value)
        return config_result

    def build_parser(self) -> ArgumentParser:
        """
        Builds the parser based on redundant implemented defaults.
        :return: prepared ArgumentParser
        """
        args = self.registered_args
        args.clear()
        actions: list[Action] = []

        parser = ArgumentParser(allow_abbrev=True)
        actions.append(parser.add_argument('-o', '--origin', metavar='origin',
                                           required=False, default=None,
                                           help='Origin path to build commit link for output'))
        actions.append(parser.add_argument('-fp', '--filepath', action='store',
                                           required=False, default=None, help='Git root to be observed'))
        actions.append(parser.add_argument('-lf', '--logfolders', metavar='Folder',
                                           required=False, default=None, type=str, nargs='+',
                                           help='Folder(s) to be observed'))
        actions.append(parser.add_argument('-ig', '--ignore', metavar='Author',
                                           required=False, type=str, nargs='+',
                                           default=None, help='Author name to be ignored'))
        actions.append(parser.add_argument('-ui', '--show-viewer', action='store_true',
                                           required=False, default=None,
                                           help='Flag to determine if application should open a grid in UI'))
        actions.append(parser.add_argument('-desc', '--descending', action='store_true',
                                           required=False, default=None,
                                           help='Flag if output should be descending. DEFAULT for --use-viewer'))
        actions.append(parser.add_argument('-cnf', '--config-file', action='store',
                                           required=False, default=None,
                                           help='Configuration file to receive application config from'))

        # Store default arguments as list in order to check against actual defaults
        for a in actions:
            args.append(a.dest)

        return parser

    def has_config(self) -> bool:
        config = self.parse_config()
        return len(config.__dict__) > 0
