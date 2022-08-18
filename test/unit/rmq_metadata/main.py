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


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_dir_chk
        arg_require
        get_args

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()
        self.opt_req = None
        self.opt_req2 = True
        self.dir_perms_chk = None
        self.dir_perms_chk2 = True

    def arg_dir_chk(self, dir_perms_chk):

        """Method:  arg_dir_chk

        Description:  Method stub holder for gen_class.ArgParser.arg_dir_chk.

        Arguments:

        """

        self.dir_perms_chk = dir_perms_chk

        return self.dir_perms_chk2

    def arg_require(self, opt_req):

        """Method:  arg_require

        Description:  Method stub holder for gen_class.ArgParser.arg_require.

        Arguments:

        """

        self.opt_req = opt_req

        return self.opt_req2

    def get_args(self):

        """Method:  get_args

        Description:  Method stub holder for gen_class.ArgParser.get_args.

        Arguments:

        """

        return self.args_array


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_help_true
        test_help_false
        test_arg_require_false
        test_arg_require_true
        test_arg_dir_chk_false
        test_arg_dir_chk_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.func_dict = {"-M": rmq_metadata.monitor_queue}

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.gen_class.ArgParser")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_help_true

        Description:  Test main function with Help_Func returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.gen_class.ArgParser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_help_false

        Description:  Test main function with Help_Func returns False.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.gen_class.ArgParser")
    def test_arg_require_false(self, mock_arg, mock_help):

        """Function:  test_arg_require_false

        Description:  Test with arg_require returns false.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.gen_class.ArgParser")
    def test_arg_require_true(self, mock_arg, mock_help):

        """Function:  test_arg_require_true

        Description:  Test with arg_require returns true.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.gen_class.ArgParser")
    def test_arg_dir_chk_false(self, mock_arg, mock_help):

        """Function:  test_arg_dir_chk_false

        Description:  Test with arg_dir_chk returns false.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.run_program")
    @mock.patch("rmq_metadata.gen_libs.help_func")
    @mock.patch("rmq_metadata.gen_class.ArgParser")
    def test_arg_dir_chk_true(self, mock_arg, mock_help, mock_run):

        """Function:  test_arg_dir_chk_true

        Description:  Test with arg_dir_chk returns true.

        Arguments:

        """

        self.args.dir_perms_chk2 = True

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_run.return_value = True

        self.assertFalse(rmq_metadata.main())


if __name__ == "__main__":
    unittest.main()
