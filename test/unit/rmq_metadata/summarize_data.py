#!/usr/bin/python
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

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import rmq_metadata
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_empty_categorized_text -> Test with empty categorized_text list.
        test_summarize_data -> Test with summarize data returned.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.token_types = ["LOCATION", "PERSON", "ORGANIZATION"]
        self.categorized_text = [(u',', u'O'), (u'London', u'LOCATION'),
                                 (u',', u'O'), (u'SW1W9AX', u'O')]
        self.categorized_text2 = [(u',', u'O'), (u'London', u'LOCATION'),
                                  (u',', u'O'), (u'SW1W9AX', u'LOCATION')]
        self.loop1 = ("O", [], [])
        self.loop2 = ("LOCATION", [], [(u'London', u'LOCATION')])
        self.loop3 = ("O", [(u'London', u'LOCATION')], [])
        self.loop4 = ("O", [(u'London', u'LOCATION')], [])
        self.loop4A = ("O", [(u'London', u'LOCATION')],
                       [(u'SW1W9AX', u'LOCATION')])
        self.data_list = [(u'London', u'LOCATION'), (u'SW1W9AX', u'LOCATION')]
        self.results = [(u'London', u'LOCATION')]
        self.results2 = [(u'London', u'LOCATION'), (u'SW1W9AX', u'LOCATION')]

    @mock.patch("rmq_metadata.merge_data")
    @mock.patch("rmq_metadata._sort_data")
    def test_end_loop_data(self, mock_sort, mock_merge):

        """Function:  test_end_loop_data

        Description:  Test with data in tmp_data at end of loop.

        Arguments:

        """

        mock_sort.side_effect = [self.loop1, self.loop2, self.loop3,
                                 self.loop4A]
        mock_merge.return_value = self.data_list

        self.assertEqual(rmq_metadata.summarize_data(
            self.categorized_text2, self.token_types), self.results2)

    def test_empty_categorized_text(self):

        """Function:  test_empty_categorized_text

        Description:  Test with empty categorized_text list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.summarize_data([], self.token_types), [])

    @mock.patch("rmq_metadata._sort_data")
    def test_summarize_data(self, mock_sort):

        """Function:  test_summarize_data

        Description:  Test with summarize data returned.

        Arguments:

        """

        mock_sort.side_effect = [self.loop1, self.loop2, self.loop3,
                                 self.loop4]

        self.assertEqual(rmq_metadata.summarize_data(
            self.categorized_text, self.token_types), self.results)


if __name__ == "__main__":
    unittest.main()
