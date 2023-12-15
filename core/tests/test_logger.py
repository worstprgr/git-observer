import unittest

import core.unittestutils
import core.logger
import core.tests.logger_factory


ut_utils = core.unittestutils.UTUtils()
logger_fact = core.tests.logger_factory.LoggerFactory()


class TestLogger(unittest.TestCase):
    def test_if_log_exists_today(self):
        """
        Checking if the log file gets created, when it's missing.\n
        Checking if the method returns `0`, if the log file exists.
        """
        # Init
        log = core.logger.Logger(__name__)

        # Given
        log_file = logger_fact.create_log_file_path()

        # When
        # Explanation: The first line creates the log file.
        # The second line checks, if the log file was created. If not, the assertion will fail.
        log.if_log_exists_today(log_file)
        log_file_existing = log.if_log_exists_today(log_file)

        # Then
        self.assertEqual(0, log_file_existing, 'Log file was not created')

        # Delete dummy file
        log.close_logger()
        ut_utils.delete_file(log_file)


if __name__ == '__main__':
    unittest.main()
