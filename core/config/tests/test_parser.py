import unittest

from core.config.parser import IniConfigParser, ArgConfigParser
from core.paths import Paths
from core.unittestutils import UTUtils
from core.config.tests.factory import ManagementFactory
from devtools.tools.ispycharm import is_pycharm_active

c_paths = Paths()
ut_utils = UTUtils()


class TestIniConfigParser(unittest.TestCase):
    def test_has_config(self):
        """
        Testing the correct boolean output, the config file exists or not.
        """
        # Given
        the_existing_file = c_paths.CONF_INI_DUMMY
        ut_utils.create_file(the_existing_file)
        file_exists = IniConfigParser(None, c_paths.CONF_INI_DUMMY)
        file_not_exist = IniConfigParser(None)

        # When
        check_file_a = file_exists.has_config()
        check_file_b = file_not_exist.has_config()

        # Then
        self.assertEqual(True, check_file_a)
        self.assertEqual(False, check_file_b)

        # Delete files
        ut_utils.delete_file(the_existing_file)

    def test_install(self):
        """
        Testing, if a config file is created.
        Testing, if the method returns `None` if a config file exists.
        """
        # Init
        cm = ManagementFactory()
        icp = IniConfigParser(cm.config_defaults)

        # Given
        icp.install()  # Set up config file

        # When
        check_if_config_exists = ut_utils.file_exists(c_paths.CONFIG_INI)
        check_if_method_gets_it_too = icp.install()

        # Then
        self.assertEqual(True, check_if_config_exists)
        self.assertEqual(None, check_if_method_gets_it_too)

        # Delete files
        ut_utils.delete_file(c_paths.CONFIG_INI)

    def test_parse_config(self):
        """
        Testing for an exception, if the config file is invalid.
        Testing the integrity and the correct output of the method.
        """
        # Init
        cm = ManagementFactory()

        # Given
        config_defaults = cm.config_defaults
        IniConfigParser(config_defaults).install()
        icp_no_valid_file = IniConfigParser(0, c_paths.CONF_INI_DUMMY)
        icp_has_valid_file = IniConfigParser(config_defaults).parse_config()

        # When
        del config_defaults['ignore']
        integrity_check = ut_utils.if_all_lines_begin_with(namespace=icp_has_valid_file, keywords=config_defaults)

        # Then
        self.assertEqual(True, integrity_check)

        with self.assertRaises(RuntimeError):
            icp_no_valid_file.parse_config()

        # Delete files
        ut_utils.delete_file(c_paths.CONFIG_INI)


# Testing Argparse using PyCharm results in weird errors, because the wrapped UT runner
# from PyCharm, conflicts here. So skipping this test if IDE = PyCharm.
#
# This tests works outside PyCharm.
@unittest.skipIf(is_pycharm_active(), 'Skipping if IDE is PyCharm.')
class TestArgConfigParser(unittest.TestCase):
    def test_build_parser(self):
        """
        Testing the integrity of the argparse return.
        Comparing the provided arguments against the output from argparse.
        """
        # Init
        cm = ManagementFactory()
        acp = ArgConfigParser(cm.config_defaults).build_parser()

        # Given
        all_args = acp.parse_args().__dict__.keys()

        # Plain arguments, without the prepended '--'
        all_available_args_for_cmp = [key for key in all_args]

        # Replacing underscores with hyphens, because `parse_args()` returns variables, not the actual names.
        # Ex.: Argument "--show-viewer" is returned as "--show_viewer".
        all_available_args = ['--' + key.replace('_', '-') for key in all_available_args_for_cmp]

        test_arguments = [
            'testorigin',
            'testfp',
            ['testlog1', 'testlog2'],
            ['testignore1', 'testignore2'],
            True,
            True,
            'testconfig.file'
        ]

        test_parser = cm.zip_options_with_args(test_arguments, all_available_args)

        # When
        cmp_argparse_in_out = cm.cmp_inp_vs_out(acp, test_parser, test_arguments, all_available_args_for_cmp)

        # Then
        self.assertEqual(True, cmp_argparse_in_out)


if __name__ == '__main__':
    unittest.main()
