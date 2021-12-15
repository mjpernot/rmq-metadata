#!/usr/bin/python
# Classification (U)

"""Program:  _validate_files.py

    Description:  Integration testing of _validate_files in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/_validate_files.py

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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_stanford_jar_path_false
        test_stanford_jar_path_true
        test_stanford_jar_false
        test_stanford_jar_true
        test_lang_module_path_false
        test_lang_module_path_true
        test_lang_module_false
        test_lang_module_true
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.tmp4 = "Error:  File %s does not exist.\n"
        self.tmp5 = "Error: File %s is not writeable.\n"
        self.tmp6 = "Error: File %s is not readable."

        self.err_msg = "Error: File /mytmp/fake_lang_module is not readable."
        integration_dir = "test/integration/rmq_metadata"
        base_path = os.path.join(os.getcwd(), integration_dir)
        config_dir = os.path.join(base_path, "config")
        self.cfg = gen_libs.load_module("rabbitmq", config_dir)
        self.status = True
        self.msg = ""
        self.err_msg = "/mytmp/fake_lang_module"
        self.err_msg2 = "lang_module not set to absolute path: ./%s" % \
                        self.cfg.lang_module
        self.err_msg3 = "/mytmp/fake_jar"
        self.err_msg4 = "stanford_jar not set to absolute path: ./%s" % \
                        self.cfg.stanford_jar

    def test_stanford_jar_path_false(self):

        """Function:  test_stanford_jar_path_false

        Description:  Test stanford_jar path check is False.

        Arguments:

        """

        self.cfg.stanford_jar = "./" + self.cfg.stanford_jar

        status, err_msg = rmq_metadata._validate_files(self.cfg, self.status,
                                                       self.msg)

        self.assertEqual((status, err_msg), (False, self.err_msg4))

    def test_stanford_jar_path_true(self):

        """Function:  test_stanford_jar_path_true

        Description:  Test if stanford_jar path check is True.

        Arguments:

        """

        status, err_msg = rmq_metadata._validate_files(self.cfg, self.status,
                                                       self.msg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_stanford_jar_false(self):

        """Function:  test_stanford_jar_false

        Description:  Test if stanford_jar check returns False.

        Arguments:

        """

        self.cfg.stanford_jar = self.err_msg3
        full_msg = self.tmp4 % self.err_msg3 + self.tmp6 % self.err_msg3

        status, err_msg = rmq_metadata._validate_files(self.cfg, self.status,
                                                       self.msg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_stanford_jar_true(self):

        """Function:  test_stanford_jar_true

        Description:  Test if stanford_jar check returns True.

        Arguments:

        """

        status, err_msg = rmq_metadata._validate_files(self.cfg, self.status,
                                                       self.msg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_lang_module_path_false(self):

        """Function:  test_lang_module_path_false

        Description:  Test if lang_module path check is False.

        Arguments:

        """

        self.cfg.lang_module = "./" + self.cfg.lang_module

        status, err_msg = rmq_metadata._validate_files(self.cfg, self.status,
                                                       self.msg)

        self.assertEqual((status, err_msg), (False, self.err_msg2))

    def test_lang_module_path_true(self):

        """Function:  test_lang_module_path_true

        Description:  Test if lang_module path check is True.

        Arguments:

        """

        status, err_msg = rmq_metadata._validate_files(self.cfg, self.status,
                                                       self.msg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_lang_module_false(self):

        """Function:  test_lang_module_false

        Description:  Test if lang_module check returns False.

        Arguments:

        """

        self.cfg.lang_module = self.err_msg
        full_msg = self.tmp4 % self.err_msg + self.tmp6 % self.err_msg

        status, err_msg = rmq_metadata._validate_files(self.cfg, self.status,
                                                       self.msg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_lang_module_true(self):

        """Function:  test_lang_module_true

        Description:  Test if lang_module check returns True.

        Arguments:

        """

        status, err_msg = rmq_metadata._validate_files(self.cfg, self.status,
                                                       self.msg)

        self.assertEqual((status, err_msg), (True, ""))

    def tearDown(self):

        """Function:  tearDown

        Description:  Cleanup of test environment.

        Arguments:

        """

        del sys.modules["rabbitmq"]


if __name__ == "__main__":
    unittest.main()
