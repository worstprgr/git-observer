import argparse
import unittest

import core.config
import core.paths as c_paths
import core.unittestutils
import core.tests.config_factory

ut_utils = core.unittestutils.UTUtils()
ut_utils_ns = core.unittestutils


class TestFunctions(unittest.TestCase):
    def test_parse_value(self):
        """
        Tests if a string value got converted correctly, to a specific type.\n
        - String with commas -> converts into a stripped list
        - Non-empty string -> converts into a positive boolean
        - Digit as string -> converts into the corresponding integer
        - Dummy Dict -> tests, if no conversion happened
        """
        cfg = core.config

        # Given
        test_list = ' Hallo ,Hello, Hi, Yo', []
        test_boolean = 'Test', True
        test_int = '10', 1
        test_other_type = 2, {}

        # When
        convert_str_to_list = cfg.parse_value(test_list[0], test_list[1])
        convert_str_to_bool = cfg.parse_value(test_boolean[0], test_boolean[1])
        convert_str_to_int = cfg.parse_value(test_int[0], test_int[1])
        no_conversion = cfg.parse_value(test_other_type[0], test_other_type[1])

        # Then
        self.assertEqual(['Hallo', 'Hello', 'Hi', 'Yo'], convert_str_to_list)
        self.assertEqual(True, convert_str_to_bool)
        self.assertEqual(10, convert_str_to_int)
        self.assertEqual(2, no_conversion)


class TestConfigHandler(unittest.TestCase):
    def test_config_exists(self):
        """
        Tests if a config file is or isn't existing.
        """
        # Init
        cfg_handler_1 = core.config.ConfigHandler()
        cfg_handler_2 = core.config.ConfigHandler()
        the_existing_file = c_paths.CONF_INI_DUMMY
        ut_utils.create_file(the_existing_file)

        # Given
        cfg_handler_1.config_ini_file = 'dude_wheres_my_file.test'
        cfg_handler_2.config_ini_file = the_existing_file

        # When
        file_does_not_exist = cfg_handler_1.config_exists()
        file_exists = cfg_handler_2.config_exists()

        # Then
        self.assertEqual(False, file_does_not_exist)
        self.assertEqual(True, file_exists)

        # Delete test file
        ut_utils.delete_file(the_existing_file)

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

    def test_parse_arguments(self):
        """
        Test not implemented.
        """
        # TODO @worstprgr: UT for Argparse (after separating the logic in `parse_arguments`)
        self.assertEqual(1, 1)

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

    def test_get_app_config(self):
        """
        Contains no test, since it would cascade methods, that are already tested.
        """
        # Init
        # Given
        # When
        # Then
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
