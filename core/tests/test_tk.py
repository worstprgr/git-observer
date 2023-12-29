import unittest

from core.tkinter.util import TkUtil


class TkUtilTest(unittest.TestCase):
    """
    UnitTest class to test TkUtil functionalities
    """
    def test_internal_calc_geometry(self):
        """
        Test, if position calculation based on given
        area dimensions and a desired size results in a centered position,
        related to desired end dimensions of dialog
        :return: None
        """
        # Given are HD screen dimensions
        screen_w = 1920
        screen_h = 1080
        # And dimensions of a form that should be shown
        form_w = 250
        form_h = 150

        # The expected result is based on the fact that a location is top left corner
        # This means:
        # X = half of screen width minus half of desired form width
        # Y = half of screen height minus half of desired form height
        # And results in given expectation string
        expected_geo_location = '250x150+835+465'

        # When calculating geometry using internal function
        calc_result = TkUtil.__calculate_geometry__(screen_w, screen_h, form_w, form_h)
        # It is expected that these rules are applied and result is exactly the same as expected
        self.assertEqual(expected_geo_location, calc_result,
                         'Expected to calculate correct form dimenstions and top left corner position')


if __name__ == '__main__':
    unittest.main()
