# Classification (U)

"""Program:  create_metadata.py

    Description:  Unit testing of create_metadata in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/create_metadata.py

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
        test_multiple_sets2
        test_multiple_sets
        test_duplicate_value
        test_add_to_key
        test_create_new_key2
        test_create_new_key
        test_empty_data_list

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.metadata = {}
        self.data = []
        self.results = {}

        self.name = 'United Kingdom'
        self.metadata2 = {'LOCATION': ['London']}
        self.data2 = [('London', 'LOCATION')]
        self.data3 = [('Steve Jones', 'PERSON')]
        self.data4 = [(self.name, 'LOCATION')]
        self.data5 = [
            ('London', 'LOCATION'), (self.name, 'LOCATION')]
        self.results2 = {'LOCATION': ['London']}
        self.results3 = {
            'PERSON': ['Steve Jones'], 'LOCATION': ['London']}
        self.results4 = {'LOCATION': ['London', self.name]}

    def test_multiple_sets2(self):

        """Function:  test_multiple_sets2

        Description:  Test with adding multiple sets.

        Arguments:

        """

        self.assertEqual(rmq_metadata.create_metadata(
            self.metadata2, self.data5), self.results4)

    def test_multiple_sets(self):

        """Function:  test_multiple_sets

        Description:  Test with adding multiple sets.

        Arguments:

        """

        self.assertEqual(rmq_metadata.create_metadata(
            self.metadata, self.data5), self.results4)

    def test_duplicate_value(self):

        """Function:  test_duplicate_value

        Description:  Test with duplicate value in list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.create_metadata(
            self.metadata2, self.data2), self.results2)

    def test_add_to_key(self):

        """Function:  test_add_to_key

        Description:  Test with adding to existing key.

        Arguments:

        """

        self.assertEqual(rmq_metadata.create_metadata(
            self.metadata2, self.data4), self.results4)

    def test_create_new_key2(self):

        """Function:  test_create_new_key2

        Description:  Test with empty data list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.create_metadata(
            self.metadata2, self.data3), self.results3)

    def test_create_new_key(self):

        """Function:  test_create_new_key

        Description:  Test with empty data list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.create_metadata(
            self.metadata, self.data2), self.results2)

    def test_empty_data_list(self):

        """Function:  test_empty_data_list

        Description:  Test with empty data list.

        Arguments:

        """

        self.assertEqual(rmq_metadata.create_metadata(
            self.metadata, self.data), self.results)


if __name__ == "__main__":
    unittest.main()
