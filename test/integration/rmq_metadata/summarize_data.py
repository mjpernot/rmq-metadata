# Classification (U)

"""Program:  summarize_data.py

    Description:  Integration testing of summarize_data in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/summarize_data.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import rmq_metadata                             # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_empty_categorized_text
        test_summarize_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.token_types = ["LOCATION", "PERSON", "ORGANIZATION"]

        self.categorized_text = [
            (',', 'O'), ('London', 'LOCATION'), (',', 'O'), ('SW1W9AX', 'O')]
        self.categorized_text2 = [
            (',', 'O'), ('London', 'LOCATION'), (',', 'O'),
            ('SW1W9AX', 'LOCATION')]
        self.results = [('London', 'LOCATION')]
        self.results2 = [('London', 'LOCATION'), ('SW1W9AX', 'LOCATION')]

    def test_end_loop_data(self):

        """Function:  test_end_loop_data

        Description:  Test with data in tmp_data at end of loop.

        Arguments:

        """

        self.assertEqual(rmq_metadata.summarize_data(
            self.categorized_text2, self.token_types), self.results2)

    def test_empty_categorized_text(self):

        """Function:  test_empty_categorized_text

        Description:  Test with empty categorized_text list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.summarize_data([], self.token_types), [])

    def test_summarize_data(self):

        """Function:  test_summarize_data

        Description:  Test with summarize data returned.

        Arguments:

        """

        self.assertEqual(rmq_metadata.summarize_data(
            self.categorized_text, self.token_types), self.results)


if __name__ == "__main__":
    unittest.main()
