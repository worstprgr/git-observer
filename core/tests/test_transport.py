import unittest
from datetime import datetime

from core.transport import ObservationUtil, Commit
from core.transport import Observation


class CommitParseFormattedTest(unittest.TestCase):
    """
    Test class for parsing commit lines into Commit transport objects
    """
    COMMIT_AUTHOR: str = 'Pitcher Seven'
    COMMIT_DATE_STR: str = '2024-01-01T00:00:00+01:00'
    COMMIT_MSG: str = 'This is a so called "UnitTest"\nIt should ensure everything\r\nworks as \'\'expected'
    COMMIT_SH1: str = '3a2f6a6a8e1'
    COMMIT_BRANCH: str = 'origin/unit-test-in-the-wild'
    DUMMY_COMMIT_LINE: str = (f'{COMMIT_AUTHOR}|{COMMIT_DATE_STR}|'
                              f'{COMMIT_MSG}|{COMMIT_SH1}|{COMMIT_BRANCH}')

    def test_commit_parsing_author(self):
        """
        Test if author is transferred correctly to
        result Commit transport object
        :return: None
        """
        # Given is an author used in dummy commit message
        commit_author = self.COMMIT_AUTHOR

        # When parsing commit using static GitObserver parse function
        commit = ObservationUtil.parse_commit_formatted(self.DUMMY_COMMIT_LINE)

        # It is expected that the commit date is the same as passed in DUMMY_COMMIT_LINE
        self.assertEqual(commit_author, commit.author,
                         "Expected to receive same commit author like passed in commit message defined")

    def test_commit_parsing_date(self):
        """
        Test if commit date is parsed and transferred correctly to
        result Commit transport object
        :return: None
        """
        # Given is a pared datetime used as string in dummy commit message
        commit_dummy_date = datetime.fromisoformat(self.COMMIT_DATE_STR)

        # When parsing commit using static GitObserver parse function
        commit = ObservationUtil.parse_commit_formatted(self.DUMMY_COMMIT_LINE)

        # It is expected that the commit date is the same as passed in DUMMY_COMMIT_LINE
        self.assertEqual(commit_dummy_date, commit.date,
                         "Expected to receive parsed date like passed in commit message defined")

    def test_commit_parsing_message(self):
        """
        Test if commit message is transferred correctly to
        result Commit transport object
        :return: None
        """
        # Given is a message used in dummy commit message
        commit_msg = self.COMMIT_MSG

        # When parsing commit using static GitObserver parse function
        commit = ObservationUtil.parse_commit_formatted(self.DUMMY_COMMIT_LINE)

        # It is expected that the commit date is the same as passed in DUMMY_COMMIT_LINE
        self.assertEqual(commit_msg, commit.message,
                         "Expected to receive same commit message like passed in commit defined")

    def test_commit_parsing_sha1(self):
        """
        Test if commit SHA1 is transferred correctly to
        result Commit transport object
        :return: None
        """
        # Given is a SHA1 used in dummy commit message
        commit_sha1 = self.COMMIT_SH1

        # When parsing commit using static GitObserver parse function
        commit = ObservationUtil.parse_commit_formatted(self.DUMMY_COMMIT_LINE)

        # It is expected that the commit date is the same as passed in DUMMY_COMMIT_LINE
        self.assertEqual(commit_sha1, commit.sha1,
                         "Expected to receive same commit SHA1 like passed in commit defined")

    def test_commit_parsing_branch(self):
        """
        Test if optional commit branch name is transferred correctly to
        result Commit transport object
        :return: None
        """
        # Given is a SHA1 used in dummy commit message
        commit_branch = self.COMMIT_BRANCH

        # When parsing commit using static GitObserver parse function
        commit = ObservationUtil.parse_commit_formatted(self.DUMMY_COMMIT_LINE)

        # It is expected that the commit date is the same as passed in DUMMY_COMMIT_LINE
        self.assertEqual(commit_branch, commit.branch,
                         "Expected to receive same commit branch name like passed in commit defined")

    def test_commit_parsing_raises(self):
        """
        Test if wrong commit line format leads to an ValueError exception
        :return: None
        """
        # Given is some garbage we want to extract a Commit object from
        message = "WRONG|FORMAT#PROVIDED~HERE"

        # This garbage is expected to raise a ValueError since parsing cannot take place with that
        with self.assertRaises(ValueError):
            ObservationUtil.parse_commit_formatted(message)


class EmptyObservationTest(unittest.TestCase):
    """
    UnitTest class for observation list helper is_empty
    """

    def test_empty_list_empty(self):
        """
        Test if an empty list[Observation] is identified as empty
        using is_empty
        :return: None
        """
        # Giving is an empty list
        empty_list: list[Observation] = []

        # When asking util if None is an empty observation list
        is_empty = ObservationUtil.is_empty(empty_list)

        # It is expected to be True since it in fact is empty
        self.assertTrue(is_empty, 'Expected empty list being a empty list[Observation]')

    def test_nested_empty_list_empty(self):
        """
        Test if a list[Observation] having one item with a empty list[Commit]
        is identified as empty using is_empty
        :return: None
        """
        # Giving is a list with one empty observation
        empty_list: list[Observation] = [Observation("Test", [])]

        # When asking util if it is an empty observation list
        is_empty = ObservationUtil.is_empty(empty_list)

        # It is expected to be True since even if there is a list, its object is empty
        self.assertTrue(is_empty, 'Expected nested empty list being a empty list[Observation]')

    def test_nested_list_not_empty(self):
        """
        Test if a list[Observation] having one item with one Commit in list[Commit]
        is identified as non-empty using is_empty
        :return: None
        """
        # Giving is None
        filled_list: list[Observation] = [
            Observation("Test",
                        [
                            Commit('Test', datetime.now(), 'Message', "ABC1234")
                        ])
        ]

        # When asking util if None is an empty observation list
        is_empty = ObservationUtil.is_empty(filled_list)

        self.assertFalse(is_empty, 'Expected nested list being a non-empty list[Observation]')


if __name__ == '__main__':
    unittest.main()
