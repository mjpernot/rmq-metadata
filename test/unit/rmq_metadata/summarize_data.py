# Classification (U)

"""Program:  summarize_data.py

    Description:  Unit testing of summarize_data in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/summarize_data.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

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
        self.loop1 = ("O", [], [])

        self.categorized_text = [
            (',', 'O'), ('London', 'LOCATION'), (',', 'O'), ('SW1W9AX', 'O')]
        self.categorized_text2 = [
            (',', 'O'), ('London', 'LOCATION'), (',', 'O'),
            ('SW1W9AX', 'LOCATION')]
        self.loop2 = ("LOCATION", [], [('London', 'LOCATION')])
        self.loop3 = ("O", [('London', 'LOCATION')], [])
        self.loop4 = ("O", [('London', 'LOCATION')], [])
        self.loop4a = (
            "O", [('London', 'LOCATION')], [('SW1W9AX', 'LOCATION')])
        self.data_list = [('London', 'LOCATION'), ('SW1W9AX', 'LOCATION')]
        self.results = [('London', 'LOCATION')]
        self.results2 = [('London', 'LOCATION'), ('SW1W9AX', 'LOCATION')]

    @mock.patch("rmq_metadata.merge_data")
    @mock.patch("rmq_metadata.sort_data")
    def test_end_loop_data(self, mock_sort, mock_merge):

        """Function:  test_end_loop_data

        Description:  Test with data in tmp_data at end of loop.

        Arguments:

        """

        mock_sort.side_effect = [self.loop1, self.loop2, self.loop3,
                                 self.loop4a]
        mock_merge.return_value = self.data_list

        self.assertEqual(
            rmq_metadata.summarize_data(
                self.categorized_text2, self.token_types), self.results2)

    def test_empty_categorized_text(self):

        """Function:  test_empty_categorized_text

        Description:  Test with empty categorized_text list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.summarize_data([], self.token_types), [])

    @mock.patch("rmq_metadata.sort_data")
    def test_summarize_data(self, mock_sort):

        """Function:  test_summarize_data

        Description:  Test with summarize data returned.

        Arguments:

        """

        mock_sort.side_effect = [self.loop1, self.loop2, self.loop3,
                                 self.loop4]

        self.assertEqual(
            rmq_metadata.summarize_data(
                self.categorized_text, self.token_types), self.results)


if __name__ == "__main__":
    unittest.main()
