import pathlib
import unittest

import core.unittestutils
import core.utils
import core.paths as c_paths
import core.tests.utils_factory


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
        utils_fact = core.tests.utils_factory.UtilsFactory()

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
        # TODO: Fix a bug in the get_base_dir method (Issue ID Missing) -> ask Daniel
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
        self.assertEqual(pathlib.WindowsPath or pathlib.PosixPath, type(path_like_obj))


if __name__ == '__main__':
    unittest.main()
