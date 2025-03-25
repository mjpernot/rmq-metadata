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
import rmq_metadata                             # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

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

        self.data_list2 = [('Ipswich', 'LOCATION')]
        self.tmp_data = [('London', 'LOCATION')]
        self.tmp_data2 = [
            ('London', 'LOCATION'), ('SW1W9AX', 'LOCATION')]
        self.tmp_data3 = [
            ('High_Road', 'LOCATION'), ('London', 'LOCATION'),
            ('SW1W9AX', 'LOCATION')]
        self.results = [('London', 'LOCATION')]
        self.results2 = [('London SW1W9AX', 'LOCATION')]
        self.results3 = [('High_Road London SW1W9AX', 'LOCATION')]
        self.results4 = [('Ipswich', 'LOCATION'), ('London', 'LOCATION')]
        self.results5 = [
            ('Ipswich', 'LOCATION'), ('London SW1W9AX', 'LOCATION')]
        self.results6 = [
            ('Ipswich', 'LOCATION'),
            ('High_Road London SW1W9AX', 'LOCATION')]

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
