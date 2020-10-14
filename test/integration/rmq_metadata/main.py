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
import lib.gen_libs as gen_libs
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
        self.integration_dir = "test/integration/rmq_metadata"
        base_path = os.path.join(os.getcwd(), self.integration_dir)
        self.config_dir = os.path.join(base_path, "config")
        base_program = os.path.join(base_path, main)
        self.cmdline = gen_libs.get_inst(sys)

        self.argv_list = [base_program, "-c", "rabbitmq", "-d",
                          self.config_dir, "-M"]

    def test_help_true(self):

        """Function:  test_status_true

        Description:  Test main function with Help_Func returns True.

        Arguments:

        """

        self.argv_list.append("-h")
        self.cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(rmq_metadata.main())

    def test_help_false(self):

        """Function:  test_status_false

        Description:  Test main function with Help_Func returns False.

        Arguments:

        """

        self.argv_list.remove("-c")
        self.argv_list.remove("rabbitmq")
        self.cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(rmq_metadata.main())

    def test_require_true_chk_true(self):

        """Function:  test_require_true_chk_true

        Description:  Test main function with arg_require returns True and
            arg_dir_chk_crt returns True.

        Arguments:

        """

        self.argv_list.remove("-c")
        self.argv_list.remove("rabbitmq")
        self.cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(rmq_metadata.main())

    def test_require_false_chk_true(self):

        """Function:  test_require_false_chk_true

        Description:  Test main function with arg_require returns False and
            arg_dir_chk_crt returns True.

        Arguments:

        """

        self.argv_list.remove("-d")
        self.argv_list.remove(self.config_dir)
        self.argv_list.append("-d")
        self.argv_list.append("/" + self.integration_dir)
        self.cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(rmq_metadata.main())

    def test_require_true_chk_false(self):

        """Function:  test_require_true_chk_false

        Description:  Test main function with arg_require returns True and
            arg_dir_chk_crt returns False.

        Arguments:

        """

        self.argv_list.remove("-d")
        self.argv_list.remove(self.config_dir)
        self.argv_list.append("-d")
        self.argv_list.append("/" + self.integration_dir)
        self.cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(rmq_metadata.main())

    @mock.patch("rmq_metadata.run_program", mock.Mock(return_value=True))
    def test_require_false_chk_false(self):

        """Function:  test_require_false_chk_false

        Description:  Test main function with arg_require returns False and
            arg_dir_chk_crt returns False.

        Arguments:

        """

        self.cmdline.argv = self.argv_list

        self.assertFalse(rmq_metadata.main())


if __name__ == "__main__":
    unittest.main()
