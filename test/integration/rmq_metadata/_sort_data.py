#!/usr/bin/python
# Classification (U)

"""Program:  _sort_data.py

    Description:  Integration testing of _sort_data in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/_sort_data.py

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
        test_new_type2 -> Test with new type and current_type not equal.
        test_new_type -> Test with new type and current_type not equal.
        test_item_type2 -> Test with item and current_type equal.
        test_item_type -> Test with item and current_type equal.
        test_item_other3 -> Test with item as other.
        test_item_other2 -> Test with item as other.
        test_item_other -> Test with item as other.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.item = (u'Text', u'O')
        self.item2 = (u'London', u'LOCATION')
        self.item3 = (u'SW1W9AX', u'LOCATION')
        self.item4 = (u'Smith', u'PERSON')
        self.current_type = ""
        self.current_type2 = "O"
        self.current_type3 = "LOCATION"
        self.current_type4 = "ORGANIZATION"
        self.data_list = []
        self.tmp_data = []
        self.tmp_data2 = [(u'London', u'LOCATION')]
        self.token_types = ["LOCATION", "PERSON", "ORGANIZATION"]
        self.result_type = "O"
        self.result_type2 = "LOCATION"
        self.result_type3 = "PERSON"
        self.result_list = []
        self.result_list2 = [(u'London', u'LOCATION')]
        self.result_tmp = []
        self.result_tmp2 = [(u'London', u'LOCATION')]
        self.result_tmp3 = [(u'London', u'LOCATION'),
                            (u'SW1W9AX', u'LOCATION')]
        self.result_tmp4 = [(u'Smith', u'PERSON')]

    def test_new_type2(self):

        """Function:  test_new_type2

        Description:  Test with new type and current_type not equal.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata._sort_data(
                self.item2, self.current_type, self.data_list,
                self.tmp_data, self.token_types),
            (self.result_type2, self.result_list, self.result_tmp2))

    def test_new_type(self):

        """Function:  test_new_type

        Description:  Test with new type and current_type not equal.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata._sort_data(
                self.item4, self.current_type3, self.data_list,
                self.tmp_data2, self.token_types),
            (self.result_type3, self.result_list2, self.result_tmp4))

    def test_item_type2(self):

        """Function:  test_item_type2

        Description:  Test with item and current_type equal.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata._sort_data(
                self.item3, self.current_type3, self.data_list,
                self.tmp_data2, self.token_types),
            (self.result_type2, self.result_list, self.result_tmp3))

    def test_item_type(self):

        """Function:  test_item_type

        Description:  Test with item and current_type equal.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata._sort_data(
                self.item2, self.current_type3, self.data_list,
                self.tmp_data, self.token_types),
            (self.result_type2, self.result_list, self.result_tmp2))

    def test_item_other3(self):

        """Function:  test_item_other3

        Description:  Test with item as other.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata._sort_data(
                self.item, self.current_type3, self.data_list,
                self.tmp_data2, self.token_types),
            (self.result_type, self.result_list2, self.result_tmp))

    def test_item_other2(self):

        """Function:  test_item_other2

        Description:  Test with item as other.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata._sort_data(
                self.item, self.current_type2, self.data_list,
                self.tmp_data, self.token_types),
            (self.result_type, self.result_list, self.result_tmp))

    def test_item_other(self):

        """Function:  test_item_other

        Description:  Test with item as other.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata._sort_data(
                self.item, self.current_type, self.data_list,
                self.tmp_data, self.token_types),
            (self.result_type, self.result_list, self.result_tmp))


if __name__ == "__main__":
    unittest.main()
