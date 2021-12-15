#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/main.py

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
        setUp
        test_help_true
        test_help_false
        test_require_true_chk_true
        test_require_false_chk_true
        test_require_true_chk_false
        test_require_false_chk_falsee

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = {"-c": "config_file", "-d": "config_dir", "-M": True}
        self.func_dict = {"-M": rmq_metadata.monitor_queue}

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.arg_parser.arg_parse2")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_status_true

        Description:  Test main function with Help_Func returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.arg_parser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_status_false

        Description:  Test main function with Help_Func returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.arg_parser")
    def test_require_true_chk_true(self, mock_arg, mock_help):

        """Function:  test_require_true_chk_true

        Description:  Test main function with arg_require returns True and
            arg_dir_chk_crt returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.arg_parser")
    def test_require_false_chk_true(self, mock_arg, mock_help):

        """Function:  test_require_false_chk_true

        Description:  Test main function with arg_require returns False and
            arg_dir_chk_crt returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.arg_parser")
    def test_require_true_chk_false(self, mock_arg, mock_help):

        """Function:  test_require_true_chk_false

        Description:  Test main function with arg_require returns True and
            arg_dir_chk_crt returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.run_program")
    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.arg_parser")
    def test_require_false_chk_false(self, mock_arg, mock_help, mock_run):

        """Function:  test_require_false_chk_false

        Description:  Test main function with arg_require returns False and
            arg_dir_chk_crt returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_run.return_value = True

        self.assertFalse(rmq_metadata.main())


if __name__ == "__main__":
    unittest.main()
