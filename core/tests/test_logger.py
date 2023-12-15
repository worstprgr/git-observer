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
        Checking if the method returns `True`, if the log file exists.
        """
        # Init
        log = core.logger.Logger(__name__)

        # Given
        log_file = logger_fact.create_log_file_path()

        # When
        # Explanation: The logfile was created by the first instance of `Logger()`
        # The following line checks, if the log file was created. If not, the assertion will fail.
        log_file_exists = log.if_log_exists_today(log_file)

        # Then
        self.assertEqual(True, log_file_exists, 'Log file not found')

        # Delete dummy file
        log.close_logger()
        ut_utils.delete_file(log_file)


if __name__ == '__main__':
    unittest.main()
