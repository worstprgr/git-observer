import argparse
import unittest

from core.config.parser import IniConfigParser, ArgConfigParser
from core.config.management import ConfigManager
import core.paths
import core.unittestutils


c_paths = core.paths.Paths()
ut_utils = core.unittestutils.UTUtils()
ut_utils_ns = core.unittestutils


class TestConfigHandler(unittest.TestCase):
    def test_config_exists(self):
        """
        Tests if a config file is or isn't existing.
        """
        # Prepare
        the_existing_file = c_paths.CONF_INI_DUMMY
        ut_utils.create_file(the_existing_file)

        # Given
        file_parser_non_existent = IniConfigParser(ConfigManager.config_defaults,
                                                   'dude_wheres_my_file.test')
        file_parser_existent = IniConfigParser(ConfigManager.config_defaults,
                                               the_existing_file)

        # When
        file_does_not_exist = file_parser_non_existent.has_config()
        file_exists = file_parser_existent.has_config()

        # Then
        self.assertEqual(False, file_does_not_exist)
        self.assertEqual(True, file_exists)

        # Delete test file
        ut_utils.delete_file(the_existing_file)

    @unittest.skip("Install currently not implemented")
    def test_install(self):
        """
        Checking if the config file got created, if there's no config file in first place.\n
        Checking if the keys in the content file are correct.\n
        """
        # Init
        cfg_handler = core.config.ConfigHandler()
        cfg_fact = core.tests.config_factory.ConfigFactory()

        # Given
        the_existing_file = c_paths.CONF_INI_DUMMY
        cfg_handler.config_ini_file = the_existing_file

        # When
        cfg_handler.install()  # Create the config file
        install_ini_file = cfg_handler.install()  # Now check, if it's created

        # Then
        self.assertEqual(True, ut_utils.if_all_lines_begin_with(fp=the_existing_file, keywords=cfg_fact.test_keywords),
                         'Config keys inside the `conf.ini` are not matching')
        self.assertEqual(None, install_ini_file)

        # Delete test file
        ut_utils.delete_file(the_existing_file)

    @unittest.skip("Arg check currently not implemented")
    def test_parse_arguments(self):
        """
        Test not implemented.
        """
        # TODO @worstprgr: UT for Argparse (after separating the logic in `parse_arguments`)
        self.assertEqual(1, 1)

    @unittest.skip("File args test currently not implemented")
    def test_handle_file_argument(self):
        """
        Checking if the correct type is returned. Expecting: `argparse.Namespace`
        """
        # Note: since this method calls other methods, that are tested separately,
        #       this tests focuses only on the return type.

        # Init
        cfg = core.config.ConfigHandler()

        # Given
        dummy_config_file = c_paths.CONF_INI_DUMMY
        fn_dummy_dict = {'config_file': dummy_config_file}
        file_name_dummy = ut_utils_ns.TestNamespace(fn_dummy_dict)

        # When
        returning_type = cfg.handle_file_argument(file_name_dummy)

        # Then
        self.assertEqual(argparse.Namespace, type(returning_type))

        # Delete test file
        ut_utils.delete_file(dummy_config_file)

    @unittest.skip("File corruption test currently not implemented")
    def test_parse_config_file(self):
        """
        Checking, if a `RuntimeError` occurs, if the config file is invalid.\n
        Checking, if the Namespace contains all desired entries.
        """
        # Init
        cfg_1 = core.config.ConfigHandler()
        cfg_2 = core.config.ConfigHandler()
        cfg_fact = core.tests.config_factory.ConfigFactory()

        # Given
        valid_config_file = c_paths.CONFIG_INI
        dummy_config_file = c_paths.CONF_INI_DUMMY
        cfg_fact.create_config_file(valid_config_file)
        ut_utils.create_file(dummy_config_file)
        cfg_2.config_ini_file = dummy_config_file

        # When
        returning_type = cfg_1.parse_config_file()

        # Then
        self.assertEqual(True, ut_utils.if_all_lines_begin_with(namespace=returning_type,
                                                                keywords=cfg_fact.test_keywords))
        with self.assertRaises(RuntimeError):
            cfg_2.parse_config_file()

        # Delete test file
        ut_utils.delete_file(dummy_config_file)
        ut_utils.delete_file(valid_config_file)

    @unittest.skip("No argument test currently not implemented")
    def test_no_args_fallback(self):
        """
        Checks if it returns the config namespace, if a config file is present.\n
        *Note: The integrity check for the namespace happens in `test_parse_config_file`.*\n
        Checks, if a config file gets created, if no config file is present.
        """
        # Init
        cfg_1 = core.config.ConfigHandler()
        cfg_2 = core.config.ConfigHandler()

        # Given
        dummy_config_file = c_paths.CONF_INI_DUMMY
        cfg_2.config_ini_file = dummy_config_file

        # When
        returning_type = cfg_1.no_args_fallback()
        cfg_2.no_args_fallback()

        # Then
        self.assertEqual(argparse.Namespace, type(returning_type))
        self.assertEqual(True, ut_utils.file_exists(dummy_config_file))

        # Delete test file
        ut_utils.delete_file(dummy_config_file)
        ut_utils.delete_file(c_paths.CONFIG_INI)

    @unittest.skip("Generic get_app_cong currently not implemented")
    def test_get_app_config(self):
        """
        Contains no test, since it would cascade methods, that are already tested.
        """
        # Init
        # Given
        # When
        # Then
        self.assertEqual(True, True)

    def test_consistent_arguments(self):
        # Given are the app config defaults
        defaults = ConfigManager.config_defaults
        # When we instantiate a ArgConfigParser and build the actual parser
        arg_parser = ArgConfigParser(defaults)
        default_parser = arg_parser.build_parser()
        # We expect that default_parser was successfully built
        self.assertIsNotNone(default_parser, 'Expected valid ArgumentParser object')
        # And all default keys are represented by parser, in order to have consistent redundancies
        for key in defaults.keys():
            self.assertIn(key, arg_parser.registered_args, f'Expected {key} as user argument')


if __name__ == '__main__':
    unittest.main()
