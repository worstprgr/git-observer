import unittest

from GitObserver import GitObserver
from core.paths import GITLOG_DUMMY, GITLOG_DUMMY_REDUNDANT
from core.tests.factory import GitObserverFactory
from core.config.management import ConfigManager

"""
This module tests functionality of GitObserver.
Please note that there is no UnitTest validating the contents of parsed DUMMY files, since testing
of parsing functionality is done in a more reliable manner by using one commit line hard-coded in this file
"""


class GitObserverTest(unittest.TestCase):

    def test_config_set(self):
        """
        Tests based on default config,
        if configuration is correctly applied to GitObserver
        :return: None
        """
        # Given is the default configuration provided by ObserverFactory
        default_config = ConfigManager.get_defaults()
        # Based on this a target test instance of GitObserver
        observer = GitObserver(default_config, is_test_instance=True)

        # When testing input config against observer setting after applying them
        # It is expected that those configurations are the same as initial default
        self.assertEqual(True, observer.is_test)
        self.assertEqual(default_config.origin, observer.origin)
        self.assertEqual(default_config.filepath, observer.filepath)
        self.assertEqual(default_config.logfolders, observer.logfolders)
        self.assertEqual(default_config.ignore, observer.ignore)
        self.assertEqual(default_config.descending, observer.descending)

    def test_dummy_file_read_single_observation(self):
        """
        Tests, if the dummy file contains exactly one Observation in result,
        when loaded with default configuration
        :return: None
        """
        # Given is a default GitObserver provided by GitObserverFactory
        observer = GitObserverFactory.create_default()

        # When executing run function
        observations = observer.run()
        # It is expected that the result it not None
        self.assertIsNotNone(observations, 'Expected not-None result when reading dummy commit log file')
        # It is expected that the result it not None
        self.assertEqual(1, len(observations),
                         'Expected exactly one observation in result when reading dummy commit log file')

    def test_dummy_file_read_count(self):
        """
        Tests if all dummy commits count is the same as in Observation result,
        when loading it using default GitObserver.
        Please note that the test does not test contents since parsing is tested explicitly
        :return: None
        """
        # Given is a default GitObserver provided by GitObserverFactory
        observer = GitObserverFactory.create_default()

        # Reading the file line count of dummy file represents expected result count
        with open(GITLOG_DUMMY, 'r') as dummy_file:
            num_lines = sum(1 for _ in dummy_file)

        # When executing run function
        observations = observer.run()
        # It is expected that the result count is same as file line count
        self.assertEqual(num_lines, len(observations[0].commits),
                         'Expected to get same result length as line count for dummy commit log file')

    def test_dummy_file_read_count_redundant(self):
        """
        Tests if parsing a dummy file that contains redundant information
        is correctly filtered, when loaded by default GitObserver
        :return: None
        """
        # Given is a default GitObserver provided by GitObserverFactory
        observer = GitObserverFactory.create_default()
        observer.gitlog_dummy_file = GITLOG_DUMMY_REDUNDANT

        # Reading the file line count of dummy file represents expected result count
        with open(GITLOG_DUMMY_REDUNDANT, 'r') as dummy_file:
            num_lines = sum(1 for _ in dummy_file)

        # When executing run function
        observations = observer.run()
        # It is expected that the result has fewer commits than defined in file
        self.assertTrue(num_lines > len(observations[0].commits))
        # It is expected that the result count is reduced to 5 since there are only 5 actual commits identified by SHA1
        self.assertEqual(5, len(observations[0].commits),
                         'Expected to get different result length as line count for dummy commit log file')

    def test_dummy_file_ignore(self):
        """
        Tests if the configuration of ignore author is applied
        while reading dummy commits using default GitObserver
        :return: None
        """
        # Given is a name we want to ignore in result
        ignore_name = 'otto.mustermann'
        # Given is the default configuration provided by ConfigFactory
        config = ConfigManager.get_defaults()
        # Modified to ignore otto.mustermann
        config.ignore = [ignore_name]
        # Based on this a target test instance of GitObserver
        observer = GitObserver(config, is_test_instance=True)

        # When executing run function
        observations = observer.run()
        # It is expected that the result does not contain any commit by otto.mustermann
        for obs in observations:
            for cmt in obs.commits:
                self.assertNotEqual(ignore_name, cmt.author, f'Configured to ignore {ignore_name} in log result')


class GitObserverLogCommandTest(unittest.TestCase):
    """
    UnitTest class doing the log command related tests
    """
    def test_git_log_command_base(self):
        """
        Test if log command of default GitObserver contains
        correct .git base directory path
        :return: None
        """
        # Given is a test instance of GitObserver initialized with default config
        observer = GitObserverFactory.create_default()
        # And the expected .git path in repository root
        expected_base = f'--git-dir={observer.filepath}/.git/'

        # When building git log command by test instance
        git_log_command = observer.get_git_log_cmd('Test')
        # It is expected that the command contains the .git folder as git-dir parameter
        self.assertIn(expected_base, git_log_command, 'Expected properly configured git base in git log command')

    def test_git_log_command_root(self):
        """
        Test if log command of default GitObserver contains
        correct repository root directory path
        :return: None
        """
        # Given is a test instance of GitObserver initialized with default config
        observer = GitObserverFactory.create_default()
        # And the expected repository root path
        expected_root = f'--work-tree={observer.filepath}'

        # When building git log command by test instance
        git_log_command = observer.get_git_log_cmd('Test')
        # It is expected that the command contains the repository root path parameter
        self.assertIn(expected_root, git_log_command,
                      'Expected properly configured repository root in git log command')

    def test_git_log_command_log_path(self):
        """
        Test if log command of default GitObserver contains
        correct observation directory path
        :return: None
        """
        # Given is a test instance of GitObserver initialized with default config
        observer = GitObserverFactory.create_default()
        # And the expected repository root path
        expected_log_path = f'{observer.filepath}/Test'

        # When building git log command by test instance
        git_log_command = observer.get_git_log_cmd('Test')
        # It is expected that the command contains the repository root path parameter
        self.assertIn(expected_log_path, git_log_command,
                      'Expected calling log for folder "Test" in git log command')

    def test_git_log_command_descending(self):
        """
        Test if log command of default GitObserver is sorted in reverse
        when setting flag descending = True
        :return: None
        """
        # Given is the default configuration provided by ConfigFactory
        config = ConfigManager.get_defaults()
        # Manipulated to sort descending
        config.descending = True
        # Given is also target test instance of GitObserver
        observer = GitObserver(config, is_test_instance=True)
        # And the expected flag for descending order
        expected_descending = '--reverse'

        # When building git log command by test instance
        git_log_command = observer.get_git_log_cmd('Test')
        # It is expected that the command contains expected parameter to sort in descending order
        self.assertIn(expected_descending, git_log_command,
                      'Expected log log command with parameter descending order')

    def test_git_log_command_ascending(self):
        """
        Test if log command of default GitObserver is sorted in date-order
        when setting flag descending = False
        :return: None
        """
        # Given is the default configuration provided by ConfigFactory
        config = ConfigManager.get_defaults()
        # Manipulated to sort ascending
        config.descending = False
        # Given is also target test instance of GitObserver
        observer = GitObserver(config, is_test_instance=True)
        # And the expected flag for ascending order
        expected_ascending = '--date-order'

        # When building git log command by test instance
        git_log_command = observer.get_git_log_cmd('Test')
        # It is expected that the command contains expected parameter to sort in ascending order
        self.assertIn(expected_ascending, git_log_command,
                      'Expected log log command with parameter ascending order')


class GitObserverShowCommandTest(unittest.TestCase):

    def test_git_show_command_base(self):
        """
        Test if git show command of default GitObserver contains
        correct .git base directory path
        :return: None
        """
        # Given is a test instance of GitObserver initialized with default config
        observer = GitObserverFactory.create_default()
        # And the expected .git path in repository root
        expected_base = f'--git-dir={observer.filepath}/.git/'

        # When building git show command by test instance
        git_show_command = observer.get_git_show_cmd('Test')
        # It is expected that the command contains the .git folder as git-dir parameter
        self.assertIn(expected_base, git_show_command, 'Expected properly configured git base in git show command')

    def test_git_show_command_root(self):
        """
        Test if git show command of default GitObserver contains
        correct repository root directory path
        :return: None
        """
        # Given is a test instance of GitObserver initialized with default config
        observer = GitObserverFactory.create_default()
        # And the expected repository root path
        expected_root = f'--work-tree={observer.filepath}'

        # When building git show command by test instance
        git_show_command = observer.get_git_show_cmd('Test')
        # It is expected that the command contains the repository root path parameter
        self.assertIn(expected_root, git_show_command,
                      'Expected properly configured repository root in git show command')

    def test_git_show_command_show_sha1(self):
        """
        Test if git show command of default GitObserver targets
        the correct commit identifier by SHA1
        :return: None
        """
        # Given is a test instance of GitObserver initialized with default config
        observer = GitObserverFactory.create_default()
        # And the expected repository root path
        expected_show_sha1 = '3a2f6a6a8e1'

        # When building git show command by test instance
        git_show_command = observer.get_git_show_cmd('3a2f6a6a8e1')
        # It is expected that the command contains the repository root path parameter
        self.assertIn(expected_show_sha1, git_show_command,
                      'Expected calling commit info for SHA1 "3a2f6a6a8e1" in git show command')


if __name__ == '__main__':
    unittest.main()
