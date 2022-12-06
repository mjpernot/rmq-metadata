# Classification (U)

"""Program:  merge_data.py

    Description:  Unit testing of merge_data in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/merge_data.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import rmq_metadata
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_pre_data_three_items
        test_pre_data_two_items
        test_pre_data_one_item
        test_three_items
        test_two_items
        test_single_item

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.data_list = []
        self.data_list2 = [(u'Ipswich', u'LOCATION')]
        self.tmp_data = [(u'London', u'LOCATION')]
        self.tmp_data2 = [(u'London', u'LOCATION'), (u'SW1W9AX', u'LOCATION')]
        self.tmp_data3 = [(u'High_Road', u'LOCATION'),
                          (u'London', u'LOCATION'), (u'SW1W9AX', u'LOCATION')]
        self.results = [(u'London', u'LOCATION')]
        self.results2 = [(u'London SW1W9AX', u'LOCATION')]
        self.results3 = [(u'High_Road London SW1W9AX', u'LOCATION')]
        self.results4 = [(u'Ipswich', u'LOCATION'), (u'London', u'LOCATION')]
        self.results5 = [(u'Ipswich', u'LOCATION'),
                         (u'London SW1W9AX', u'LOCATION')]
        self.results6 = [(u'Ipswich', u'LOCATION'),
                         (u'High_Road London SW1W9AX', u'LOCATION')]

    def test_pre_data_three_items(self):

        """Function:  test_pre_data_three_items

        Description:  Test with pre-data and three items in list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.merge_data(
            self.data_list2, self.tmp_data3), self.results6)

    def test_pre_data_two_items(self):

        """Function:  test_pre_data_two_items

        Description:  Test with pre-data and two items in list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.merge_data(
            self.data_list2, self.tmp_data2), self.results5)

    def test_pre_data_one_item(self):

        """Function:  test_pre_data_one_item

        Description:  Test with pre-data and one item in list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.merge_data(
            self.data_list2, self.tmp_data), self.results4)

    def test_three_items(self):

        """Function:  test_three_items

        Description:  Test with three items in list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.merge_data(
            self.data_list, self.tmp_data3), self.results3)

    def test_two_items(self):

        """Function:  test_two_items

        Description:  Test with two items in list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.merge_data(
            self.data_list, self.tmp_data2), self.results2)

    def test_single_item(self):

        """Function:  test_single_item

        Description:  Test with one item in list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.merge_data(
            self.data_list, self.tmp_data), self.results)


if __name__ == "__main__":
    unittest.main()
