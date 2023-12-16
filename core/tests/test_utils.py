import pathlib
import unittest

import core.unittestutils
from core.utils import TypeUtil
import core.paths
import core.tests.factory

c_paths = core.paths.Paths()
ut_utils = core.unittestutils.UTUtils()


class TestFileUtils(unittest.TestCase):
    def test_simple_fopen(self):
        """
        Checks following scenarios:\n
        - if read mode 0 (Default) returns a string
        - if read mode 1 returns a list
        - if a non-existing file raises `FileNotFoundError`
        - if a non-existing read mode raises `UserWarning`
        """
        # Init
        dummy_file = c_paths.BUNNY_FILE
        file_utils = core.utils.FileUtils()
        utils_fact = core.tests.factory.UtilsFactory()

        # Given
        utils_fact.create_bunny_file(dummy_file)

        # When
        mode_read = file_utils.simple_fopen(dummy_file)  # Default read_mode = 0
        mode_readlines = file_utils.simple_fopen(dummy_file, 1)

        # Then
        self.assertEqual(True, ut_utils.cmp_types(mode_read, str))
        self.assertEqual(True, ut_utils.cmp_types(mode_readlines, list))

        with self.assertRaises(FileNotFoundError):
            file_utils.simple_fopen('')

        with self.assertRaises(UserWarning):
            file_utils.simple_fopen(dummy_file, 5)

        # Delete dummy file
        ut_utils.delete_file(dummy_file)


class TestPathUtils(unittest.TestCase):
    def test_get_base_dir(self):
        # Init
        # Given
        # When
        # Then
        self.assertEqual(True, True)

    def test_conv_to_path_object(self):
        """
        Checking, if a path got correctly converted to a path-like-object.
        """
        # Init
        path_utils = core.utils.PathUtils()

        # Given
        test_path = 'testpath/test/another-test'

        # When
        path_like_obj = path_utils.conv_to_path_object(test_path)

        # Then
        self.assertTrue(isinstance(path_like_obj, (pathlib.Path, type(pathlib.Path()))))


class TestTypeUtil(unittest.TestCase):

    def test_parse_value(self):
        """
        Tests if a string value got converted correctly, to a specific type.\n
        - String with commas -> converts into a stripped list
        - Non-empty string -> converts into a positive boolean
        - Digit as string -> converts into the corresponding integer
        - Dummy Dict -> tests, if no conversion happened
        """

        # Given
        test_list = ' Hallo ,Hello, Hi, Yo', []
        test_boolean = 'Test', True
        test_int = '10', 1
        test_other_type = 2, {}

        # When
        convert_str_to_list = TypeUtil.parse_value(test_list[0], test_list[1])
        convert_str_to_bool = TypeUtil.parse_value(test_boolean[0], test_boolean[1])
        convert_str_to_int = TypeUtil.parse_value(test_int[0], test_int[1])
        # Unclear why this even works; expected is str, but we enter with int
        no_conversion = TypeUtil.parse_value(test_other_type[0], test_other_type[1])

        # Then
        self.assertEqual(['Hallo', 'Hello', 'Hi', 'Yo'], convert_str_to_list)
        self.assertEqual(True, convert_str_to_bool)
        self.assertEqual(10, convert_str_to_int)
        self.assertEqual(2, no_conversion)


if __name__ == '__main__':
    unittest.main()
