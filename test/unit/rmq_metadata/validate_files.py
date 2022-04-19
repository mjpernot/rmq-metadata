#!/usr/bin/python
# Classification (U)

"""Program:  validate_files.py

    Description:  Unit testing of validate_files in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/validate_files.py

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


class CfgTest(object):

    """Class:  CfgTest

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.host = "HOSTNAME"
        self.exchange_name = "rmq_metadata_unit_test"
        self.to_line = None
        self.port = 5672
        self.exchange_type = "direct"
        self.x_durable = True
        self.q_durable = True
        self.auto_delete = False
        self.message_dir = "message_dir"
        self.log_dir = "logs"
        self.log_file = "rmq_metadata.log"
        self.archive_dir = "/dir/path"
        self.tmp_dir = "/dir/tmp_path"
        self.lang_module = "/path/Stanford_lang_module"
        self.stanford_jar = "/path/Stanford.jar"
        self.queue_list = [
            {"queue": "rmq_metadata_unit_test",
             "routing_key": "MY_ROUTING_KEY",
             "directory": "/dir/path"}]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_stanford_jar_path_false2
        test_stanford_jar_path_false
        test_stanford_jar_path_true
        test_stanford_jar_false
        test_stanford_jar_true
        test_lang_module_path_false2
        test_lang_module_path_false
        test_lang_module_path_true
        test_lang_module_false
        test_lang_module_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.msg = ""
        self.status = True
        self.base_dir = "/BASE_DIR_PATH"
        self.err_msg5 = "Lang Module File"
        self.err_msg6 = "Stanford Jar File"
        base_name, ext_name = os.path.splitext(self.cfg.log_file)
        self.log_name = \
            base_name + "_" + self.cfg.exchange_name + "_" + ext_name

    @mock.patch("rmq_metadata.gen_libs")
    def test_stanford_jar_path_false2(self, mock_lib):

        """Function:  test_stanford_jar_path_false2

        Description:  Test stanford_jar path check is False.

        Arguments:

        """

        self.cfg.stanford_jar = "./path/Stanford.jar"
        msg = "stanford_jar not set to absolute path: %s" % \
              (self.cfg.stanford_jar)

        mock_lib.chk_crt_file.side_effect = [(True, None),
                                             (False, self.err_msg6)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (False, msg))

    @mock.patch("rmq_metadata.gen_libs")
    def test_stanford_jar_path_false(self, mock_lib):

        """Function:  test_stanford_jar_path_false

        Description:  Test stanford_jar path check is False.

        Arguments:

        """

        self.cfg.stanford_jar = "./path/Stanford.jar"
        msg = "stanford_jar not set to absolute path: %s" % \
              (self.cfg.stanford_jar)

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (False, msg))

    @mock.patch("rmq_metadata.gen_libs")
    def test_stanford_jar_path_true(self, mock_lib):

        """Function:  test_stanford_jar_path_true

        Description:  Test if stanford_jar path check is True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_stanford_jar_false(self, mock_lib):

        """Function:  test_stanford_jar_false

        Description:  Test if stanford_jar check returns False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(False, self.err_msg6),
                                             (True, None)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg6))

    @mock.patch("rmq_metadata.gen_libs")
    def test_stanford_jar_true(self, mock_lib):

        """Function:  test_stanford_jar_true

        Description:  Test if stanford_jar check returns True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_lang_module_path_false2(self, mock_lib):

        """Function:  test_lang_module_path_false2

        Description:  Test if lang_module path check is False.

        Arguments:

        """

        self.cfg.lang_module = "./path/Stanford_lang_module"
        msg = "lang_module not set to absolute path: %s" % \
              (self.cfg.lang_module) + self.err_msg5

        mock_lib.chk_crt_file.side_effect = [(False, self.err_msg5),
                                             (True, None)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (False, msg))

    @mock.patch("rmq_metadata.gen_libs")
    def test_lang_module_path_false(self, mock_lib):

        """Function:  test_lang_module_path_false

        Description:  Test if lang_module path check is False.

        Arguments:

        """

        self.cfg.lang_module = "./path/Stanford_lang_module"
        msg = "lang_module not set to absolute path: %s" % \
              (self.cfg.lang_module)

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (False, msg))

    @mock.patch("rmq_metadata.gen_libs")
    def test_lang_module_path_true(self, mock_lib):

        """Function:  test_lang_module_path_true

        Description:  Test if lang_module path check is True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_lang_module_false(self, mock_lib):

        """Function:  test_lang_module_false

        Description:  Test if lang_module check returns False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(False, self.err_msg5),
                                             (True, None)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg5))

    @mock.patch("rmq_metadata.gen_libs")
    def test_lang_module_true(self, mock_lib):

        """Function:  test_lang_module_true

        Description:  Test if lang_module check returns True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]

        status_flag, err_msg = rmq_metadata.validate_files(
            self.cfg, self.status, self.msg)

        self.assertEqual((status_flag, err_msg), (True, ""))


if __name__ == "__main__":
    unittest.main()
