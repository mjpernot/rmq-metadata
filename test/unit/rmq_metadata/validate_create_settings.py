# Classification (U)

"""Program:  validate_create_settings.py

    Description:  Unit testing of validate_create_settings in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/validate_create_settings.py

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
        self.base_dir = "/base/directory_path"
        self.message_dir = "message_dir"
        self.log_dir = "logs"
        self.log_file = "rmq_metadata.log"
        self.archive_dir = "archive"
        self.tmp_dir = "/dir/tmp_path"
        self.lang_module = "/path/Stanford_lang_module"
        self.stanford_jar = "/path/Stanford.jar"
        self.queue_list = [
            {"queue": "rmq_metadata_unit_test",
             "routing_key": "MY_ROUTING_KEY",
             "directory": "/dir/final_data"}]


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
        test_tmp_dir_false
        test_tmp_dir_not_abs
        test_tmp_dir_true
        test_archive_dir_false
        test_archive_not_abs
        test_archive_dir_true
        test_multi_queues_two_fail
        test_multi_queues_one_fail
        test_multiple_queues
        test_multiple_false2
        test_multiple_false
        test_log_dir_false
        test_log_dir_true
        test_message_dir_false
        test_message_dir_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.cfg2 = CfgTest()
        self.cfg2.queue_list.append(
            {"queue": "rmq_metadata_unit_test2", "routing_key": "ROUTING_KEY",
             "directory": "/dir/path"})
        self.base_dir = "/BASE_DIR_PATH"
        self.err_msg1 = "Missing Message Dir "
        self.err_msg2 = "Missing Log Dir "
        self.err_msg4 = "Error Queue Dir"
        self.err_msg5 = "Lang Module File"
        self.err_msg6 = "Stanford Jar File"
        base_name, ext_name = os.path.splitext(self.cfg.log_file)
        self.log_name = \
            base_name + "_" + self.cfg.exchange_name + "_" + ext_name
        self.log_name = \
            base_name + "_" + self.cfg.exchange_name + ext_name

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
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, msg))

    @mock.patch("rmq_metadata.gen_libs")
    def test_stanford_jar_path_true(self, mock_lib):

        """Function:  test_stanford_jar_path_true

        Description:  Test if stanford_jar path check is True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_stanford_jar_false(self, mock_lib):

        """Function:  test_stanford_jar_false

        Description:  Test if stanford_jar check returns False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(False, self.err_msg6),
                                             (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg6))

    @mock.patch("rmq_metadata.gen_libs")
    def test_stanford_jar_true(self, mock_lib):

        """Function:  test_stanford_jar_true

        Description:  Test if stanford_jar check returns True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

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
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, msg))

    @mock.patch("rmq_metadata.gen_libs")
    def test_lang_module_path_true(self, mock_lib):

        """Function:  test_lang_module_path_true

        Description:  Test if lang_module path check is True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_lang_module_false(self, mock_lib):

        """Function:  test_lang_module_false

        Description:  Test if lang_module check returns False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(False, self.err_msg5),
                                             (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg5))

    @mock.patch("rmq_metadata.gen_libs")
    def test_lang_module_true(self, mock_lib):

        """Function:  test_lang_module_true

        Description:  Test if lang_module check returns True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_tmp_dir_false(self, mock_lib):

        """Function:  test_tmp_dir_false

        Description:  Test if tmp_dir check returns False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (False, self.err_msg1),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg1))

    @mock.patch("rmq_metadata.gen_libs")
    def test_tmp_dir_not_abs(self, mock_lib):

        """Function:  test_tmp_dir_not_abs

        Description:  Test when tmp_dir is not abs.

        Arguments:

        """

        self.cfg.tmp_dir = "./dir/tmp_path"

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_tmp_dir_true(self, mock_lib):

        """Function:  test_tmp_dir_true

        Description:  Test if tmp_dir check returns True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_archive_dir_false(self, mock_lib):

        """Function:  test_archive_dir_false

        Description:  Test if archive_dir check returns False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (False, self.err_msg1), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg1))

    @mock.patch("rmq_metadata.gen_libs")
    def test_archive_not_abs(self, mock_lib):

        """Function:  test_archive_not_abs

        Description:  Test when archive_dir is not abs.

        Arguments:

        """

        self.cfg.archive_dir = "./dir/path"

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_archive_dir_true(self, mock_lib):

        """Function:  test_archive_dir_true

        Description:  Test if archive_dir check returns True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_multi_queues_two_fail(self, mock_lib):

        """Function:  test_multi_queues_two_fail

        Description:  Test with multi queues and two failure.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (False, self.err_msg4), (False, self.err_msg4)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg2)

        self.assertEqual((status_flag, err_msg),
                         (False, self.err_msg4 + self.err_msg4))

    @mock.patch("rmq_metadata.gen_libs")
    def test_multi_queues_one_fail(self, mock_lib):

        """Function:  test_multi_queues_one_fail

        Description:  Test with multi queues and one failure.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None), (False, self.err_msg4)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg2)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg4))

    @mock.patch("rmq_metadata.gen_libs")
    def test_multiple_queues(self, mock_lib):

        """Function:  test_multiple_queues

        Description:  Test with multiple queues.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None), (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_multiple_false2(self, mock_lib):

        """Function:  test_multiple_false

        Description:  Test if multiple checks return False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (False, self.err_msg1), (False, self.err_msg2), (True, None),
            (True, None), (False, self.err_msg4)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg),
                         (False,
                          self.err_msg1 + self.err_msg2 + self.err_msg4))

    @mock.patch("rmq_metadata.gen_libs")
    def test_multiple_false(self, mock_lib):

        """Function:  test_multiple_false

        Description:  Test if multiple checks return False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (False, self.err_msg1), (False, self.err_msg2), (True, None),
            (True, None), (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg),
                         (False, self.err_msg1 + self.err_msg2))

    @mock.patch("rmq_metadata.gen_libs")
    def test_log_dir_false(self, mock_lib):

        """Function:  test_log_dir_false

        Description:  Test if log_dir check returns False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (False, self.err_msg2), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg2))

    @mock.patch("rmq_metadata.gen_libs")
    def test_log_dir_true(self, mock_lib):

        """Function:  test_log_dir_true

        Description:  Test if log_dir check returns True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        cfg_mod, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg, cfg_mod.log_file),
                         (True, "", os.path.join(self.cfg.log_dir,
                                                 self.log_name)))

    @mock.patch("rmq_metadata.gen_libs")
    def test_message_dir_false(self, mock_lib):

        """Function:  test_message_dir_false

        Description:  Test if message_dir check returns False.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (False, self.err_msg1), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg1))

    @mock.patch("rmq_metadata.gen_libs")
    def test_message_dir_true(self, mock_lib):

        """Function:  test_message_dir_true

        Description:  Test if message_dir check returns True.

        Arguments:

        """

        mock_lib.chk_crt_file.side_effect = [(True, None), (True, None)]
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None),
            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))


if __name__ == "__main__":
    unittest.main()
