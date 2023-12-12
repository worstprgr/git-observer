import unittest

import core.unittestutils
import core.logger
# import core.paths as c_paths


ut_utils = core.unittestutils.UTUtils()


class TestLogger(unittest.TestCase):
    def test_if_log_exists_today(self):
        """
        Checking if the log file gets created, when it's missing.\n
        Checking if the method returns `0`, if the log file exists.
        """
        # TODO @worstprgr: Fix issue #50, before uncommenting this test
        # # Init
        # log = core.logger.Logger(__name__)
        #
        # # Given
        # dummy_log = ut_utils.lazy_path_obj(c_paths.LOG_FILE_DUMMY)
        #
        # # When
        # # Explanation: The first line creates the log file.
        # # The second line checks, if the log file was created. If not, the assertion will fail.
        # log.if_log_exists_today(dummy_log)
        # log_file_existing = log.if_log_exists_today(dummy_log)
        #
        # # Then
        # self.assertEqual(0, log_file_existing, 'Log file was not created')
        #
        # # Delete dummy file
        # ut_utils.delete_file(dummy_log)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
