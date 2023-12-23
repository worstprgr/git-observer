import unittest


# Test function
def addition(a: int, b: int) -> int:
    return a + b


class MyTestCase(unittest.TestCase):
    """
    This is a basic boilerplate how unit tests in Python are structured.

    Docs:
    https://docs.python.org/3/library/unittest.html
    """
    def test_something1(self):
        """
        Test Description (Mandatory)
        Assert if a and b are equal.
        """
        # Given
        the_source_of_truth = True
        method_to_test = True

        # When

        # Then
        self.assertEqual(the_source_of_truth, method_to_test)

    def test_something2(self):
        """
        Test Description (Mandatory)
        Assert if a specific exception is raised.
        """
        # Given
        a_list = ['Hello', 'Hi', 'Morning']

        # When
        # Function, that accesses the 6th item in the list (which does not exist)
        def provoke_index_error(test_list):
            return test_list[5]

        # Then
        # The assertion happens inside a `context manager`.
        # This allows to encapsulate the error.
        # Any other approach would trigger the exception before an assertion.
        # So in that case, we want to assert if an `IndexError` correctly appears.
        with self.assertRaises(IndexError):
            provoke_index_error(a_list)

    def test_dummy(self):
        """
        Test Description (Mandatory)
        Example how to work with imported modules.
        """
        # Given
        test_var1 = 5
        test_var2 = 10
        expected_result = 15

        # When
        scenario1 = addition(test_var1, test_var2)

        # Then
        self.assertEqual(expected_result, scenario1)


# This runs all tests in this file, even if we implement multiple classes.
# But you can run specific runs if you wish. You can call them inside the code like any other class.
if __name__ == '__main__':
    unittest.main()
