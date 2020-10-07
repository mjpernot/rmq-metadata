#!/usr/bin/python
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

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party

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
        test_multiple_sets2 -> Test with adding multiple sets.
        test_multiple_sets -> Test with adding multiple sets.
        test_duplicate_value -> Test with duplicate value in list.
        test_add_to_key -> Test with adding to existing key.
        test_create_new_key2 -> Test with creating new key in dictionary.
        test_create_new_key -> Test with creating new key in dictionary.
        test_empty_data_list -> Test with empty data list.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.name = u'United Kingdom'
        self.metadata = {}
        self.metadata2 = {u'LOCATION': [u'London']}
        self.data = []
        self.data2 = [(u'London', u'LOCATION')]
        self.data3 = [(u'Steve Jones', u'PERSON')]
        self.data4 = [(self.name, u'LOCATION')]
        self.data5 = [(u'London', u'LOCATION'),
                      (self.name, u'LOCATION')]
        self.results = {}
        self.results2 = {u'LOCATION': [u'London']}
        self.results3 = {u'PERSON': [u'Steve Jones'], u'LOCATION': [u'London']}
        self.results4 = {u'LOCATION': [u'London', self.name]}

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
