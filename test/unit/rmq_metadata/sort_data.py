# Classification (U)

"""Program:  sort_data.py

    Description:  Unit testing of sort_data in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/sort_data.py

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
        test_new_type2
        test_new_type
        test_item_type2
        test_item_type
        test_item_other3
        test_item_other2
        test_item_other

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.item = ('Text', 'O')
        self.item2 = ('London', 'LOCATION')
        self.item3 = ('SW1W9AX', 'LOCATION')
        self.item4 = ('Smith', 'PERSON')
        self.tmp_data2 = [('London', 'LOCATION')]
        self.result_list2 = [('London', 'LOCATION')]
        self.result_tmp2 = [('London', 'LOCATION')]
        self.result_tmp3 = [('London', 'LOCATION'), ('SW1W9AX', 'LOCATION')]
        self.result_tmp4 = [('Smith', 'PERSON')]

        self.current_type = ""
        self.current_type2 = "O"
        self.current_type3 = "LOCATION"
        self.current_type4 = "ORGANIZATION"
        self.data_list = []
        self.tmp_data = []
        self.token_types = ["LOCATION", "PERSON", "ORGANIZATION"]
        self.result_type = "O"
        self.result_type2 = "LOCATION"
        self.result_type3 = "PERSON"
        self.result_list = []
        self.result_tmp = []

    def test_new_type2(self):

        """Function:  test_new_type2

        Description:  Test with new type and current_type not equal.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.sort_data(
                self.item2, self.current_type, self.data_list,
                self.tmp_data, self.token_types),
            (self.result_type2, self.result_list, self.result_tmp2))

    def test_new_type(self):

        """Function:  test_new_type

        Description:  Test with new type and current_type not equal.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.sort_data(
                self.item4, self.current_type3, self.data_list,
                self.tmp_data2, self.token_types),
            (self.result_type3, self.result_list2, self.result_tmp4))

    def test_item_type2(self):

        """Function:  test_item_type2

        Description:  Test with item and current_type equal.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.sort_data(
                self.item3, self.current_type3, self.data_list,
                self.tmp_data2, self.token_types),
            (self.result_type2, self.result_list, self.result_tmp3))

    def test_item_type(self):

        """Function:  test_item_type

        Description:  Test with item and current_type equal.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.sort_data(
                self.item2, self.current_type3, self.data_list,
                self.tmp_data, self.token_types),
            (self.result_type2, self.result_list, self.result_tmp2))

    @mock.patch("rmq_metadata.merge_data")
    def test_item_other3(self, mock_merge):

        """Function:  test_item_other3

        Description:  Test with item as other.

        Arguments:

        """

        mock_merge.return_value = self.tmp_data2

        self.assertEqual(
            rmq_metadata.sort_data(
                self.item, self.current_type3, self.data_list,
                self.tmp_data2, self.token_types),
            (self.result_type, self.result_list2, self.result_tmp))

    def test_item_other2(self):

        """Function:  test_item_other2

        Description:  Test with item as other.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.sort_data(
                self.item, self.current_type2, self.data_list,
                self.tmp_data, self.token_types),
            (self.result_type, self.result_list, self.result_tmp))

    def test_item_other(self):

        """Function:  test_item_other

        Description:  Test with item as other.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.sort_data(
                self.item, self.current_type, self.data_list,
                self.tmp_data, self.token_types),
            (self.result_type, self.result_list, self.result_tmp))


if __name__ == "__main__":
    unittest.main()
