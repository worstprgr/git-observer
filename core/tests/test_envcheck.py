import unittest

from core.envcheck import EnvironmentCheck
from core.unittestutils import DummyNamespace
from core.tests.factory import EnvCheckFactory


ec_fact = EnvCheckFactory()


class TestEnvironmentCheck(unittest.TestCase):
    def test_folders_exists(self):
        """
        Testing if the method responds with the correct return values, if the
        essential folder structure is present or isn't.
        """
        # Given
        env_check_valid = EnvironmentCheck(disable_logging=True)
        env_check_invalid = EnvironmentCheck(disable_logging=True)

        # Overwrite the class `core.paths.Paths()` with an invalid entry
        # and convert it to a dummy namespace.
        ec_invalid_test_dirs = ec_fact.convert_list_to_dict(env_check_invalid.ignore_temp_files)
        ec_invalid_test_dirs.update({'INVALID': 'not-core'})
        env_check_invalid.c_paths_mod = DummyNamespace(ec_invalid_test_dirs)

        # When
        folders_existing = env_check_valid.folders_exists()
        folders_not_exist = env_check_invalid.folders_exists()

        # Then
        self.assertEqual(True, folders_existing)
        self.assertEqual(False, folders_not_exist)


if __name__ == '__main__':
    unittest.main()
