#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Integration testing of main in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/main.py

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
        test_help_true -> Test with Help_Func returns True.
        test_help_false -> Test with Help_Func returns False.
        test_require_true_chk_true -> Test with arg_require returns True and
            arg_dir_chk_crt returns True.
        test_require_false_chk_true -> Test with arg_require returns False and
            arg_dir_chk_crt returns True.
        test_require_true_chk_false -> Test with arg_require returns True and
            arg_dir_chk_crt returns False.
        test_require_false_chk_falsee -> Test with arg_require returns False
            and arg_dir_chk_crt returns False.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        main = "main.py"
        integration_dir = "test/integration/rmq_metadata"
        base_path = os.path.join(os.getcwd(), integration_dir)
        config_dir = os.path.join(base_path, "config")
        base_program = os.path.join(base_path, main)

        self.argv_list = [base_program, "-c", "rabbitmq", "-d", config_dir,
                          "-M"]
        STOPPED HERE

        #self.args = {"-c": "config_file", "-d": "config_dir", "-M": True}
        #self.func_dict = {"-M": rmq_metadata.monitor_queue}

    def test_help_true(self):

        """Function:  test_status_true

        Description:  Test main function with Help_Func returns True.

        Arguments:

        """

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
