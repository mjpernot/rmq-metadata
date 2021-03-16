#!/usr/bin/python
# Classification (U)

"""Program:  validate_create_settings.py

    Description:  Integration testing of validate_create_settings in
        rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/validate_create_settings.py

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
        setUp -> Initialize testing environment.
        test_multi_queues_two_fail -> Test with multi queues and two failure.
        test_multi_queues_one_fail -> Test with multi queues and one failure.
        test_multiple_queues -> Test with multiple queues.
        test_single_queue_false -> Test with single queue with dir failure.
        test_single_queue2 -> Test with single queue.
        test_single_queue -> Test with single queue.
        test_multiple_false2 -> Test if multiple checks return False.
        test_stanford_jar_path_false -> Test stanford_jar path check is False.
        test_stanford_jar_path_true2 -> Test if stanford_jar path chk is True.
        test_stanford_jar_path_true -> Test if stanford_jar path check is True.
        test_stanford_jar_false -> Test if stanford_jar check returns False.
        test_stanford_jar_true2 -> Test if stanford_jar check returns True.
        test_stanford_jar_true -> Test if stanford_jar check returns True.
        test_lang_module_path_false -> Test if lang_module path check is False.
        test_lang_module_path_true2 -> Test if lang_module path check is True.
        test_lang_module_path_true -> Test if lang_module path check is True.
        test_lang_module_false -> Test if lang_module check returns False.
        test_lang_module_true2 -> Test if lang_module check returns True.
        test_lang_module_true -> Test if lang_module check returns True.
        test_tmp_dir_false -> Test if tmp_dir check returns False.
        test_tmp_dir_not_abs2 -> Test when tmp_dir is not abs.
        test_tmp_dir_not_abs -> Test when tmp_dir is not abs.
        test_tmp_dir_true2 -> Test if tmp_dir check returns True.
        test_tmp_dir_true -> Test if tmp_dir check returns True.
        test_archive_dir_false -> Test if archive_dir check returns False.
        test_archive_not_abs2 -> Test when archive_dir is not abs.
        test_archive_not_abs -> Test when archive_dir is not abs.
        test_archive_dir_true2 -> Test if archive_dir check returns True.
        test_archive_dir_true -> Test if archive_dir check returns True.
        test_multiple_false -> Test if multiple checks return False.
        test_log_dir_false -> Test if log_dir check returns False.
        test_log_dir_true2 -> Test if log_dir check returns True.
        test_log_dir_true -> Test if log_dir check returns True.
        test_message_dir_false -> Test if message_dir check returns False.
        test_message_dir_true2 -> Test if message_dir check returns True.
        test_message_dir_true -> Test if message_dir check returns True.
        tearDown -> Cleanup of test environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.tmp = "Error: Directory: %s does not exist.\n"
        self.tmp2 = "Error: Directory %s is not writeable.\n"
        self.tmp3 = "Error: Directory %s is not readable."
        self.tmp4 = "Error:  File %s does not exist.\n"
        self.tmp5 = "Error: File %s is not writeable.\n"
        self.tmp6 = "Error: File %s is not readable."
        self.tmp7 = "stanford_jar not set to absolute path: %s"
        self.tmp8 = "lang_module not set to absolute path: %s"
        integration_dir = "test/integration/rmq_metadata"
        base_path = os.path.join(os.getcwd(), integration_dir)
        config_dir = os.path.join(base_path, "config")
        self.cfg = gen_libs.load_module("rabbitmq", config_dir)
        self.err_msg = "/mytmp/fake_message_dir"
        self.err_msg2 = "/mytmp/fake_log_dir"
        self.err_msg3 = "/mytmp/fake_archive_dir"
        self.err_msg4 = "/mytmp/fake_tmp_dir"
        self.err_msg5 = "/mytmp/fake_lang_module"
        self.err_msg7 = "/mytmp/fake_jar"
        self.err_msg9 = "/mytmp/fake_final"
        self.queue = dict(self.cfg.queue_list[0])
        self.queue["queue"] = "mail2rmq_file2"
        self.queue["routing_key"] = "mail2rmq_file2"

    def test_multi_queues_two_fail(self):

        """Function:  test_multi_queues_two_fail

        Description:  Test with multi queues and two failure.

        Arguments:

        """

        self.cfg.queue_list.append(self.queue)
        self.cfg.queue_list[0]["directory"] = self.err_msg9
        self.cfg.queue_list[1]["directory"] = self.err_msg9
        full_msg = self.tmp % self.err_msg9 + self.tmp2 % self.err_msg9 \
                   + self.tmp3 % self.err_msg9

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg + full_msg))

    def test_multi_queues_one_fail(self):

        """Function:  test_multi_queues_one_fail

        Description:  Test with multi queues and one failure.

        Arguments:

        """

        self.cfg.queue_list.append(self.queue)
        self.cfg.queue_list[0]["directory"] = self.err_msg9
        full_msg = self.tmp % self.err_msg9 + self.tmp2 % self.err_msg9 \
                   + self.tmp3 % self.err_msg9

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_multiple_queues(self):

        """Function:  test_multiple_queues

        Description:  Test with multiple queues.

        Arguments:

        """

        self.cfg.queue_list.append(self.queue)

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_single_queue_false(self):

        """Function:  test_single_queue_false

        Description:  Test with single queue with dir failure.

        Arguments:

        """

        self.cfg.queue_list[0]["directory"] = self.err_msg9
        full_msg = self.tmp % self.err_msg9 + self.tmp2 % self.err_msg9 \
                   + self.tmp3 % self.err_msg9

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_single_queue2(self):

        """Function:  test_single_queue2

        Description:  Test with single queue.

        Arguments:

        """

        final_dir = self.cfg.queue_list[0]["directory"]

        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.queue_list[0]["directory"], final_dir)

    def test_single_queue(self):

        """Function:  test_single_queue

        Description:  Test with single queue.

        Arguments:

        """

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_multiple_false2(self):

        """Function:  test_multiple_false2

        Description:  Test if multiple checks return False.

        Arguments:

        """

        self.cfg.message_dir = self.err_msg9
        self.cfg.log_dir = self.err_msg9
        self.cfg.stanford_jar = "./" + self.cfg.stanford_jar
        full_msg = self.tmp % self.err_msg9 + self.tmp2 % self.err_msg9 \
                   + self.tmp3 % self.err_msg9
        full_msg2 = self.tmp7 % self.cfg.stanford_jar

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg),
                         (False, full_msg + full_msg + full_msg2))

    def test_stanford_jar_path_false(self):

        """Function:  test_stanford_jar_path_false

        Description:  Test stanford_jar path check is False.

        Arguments:

        """

        self.cfg.stanford_jar = "./" + self.cfg.stanford_jar
        full_msg = self.tmp7 % self.cfg.stanford_jar

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_stanford_jar_path_true2(self):

        """Function:  test_stanford_jar_path_true2

        Description:  Test if stanford_jar path check is True.

        Arguments:

        """

        stanford_jar = self.cfg.stanford_jar

        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.stanford_jar, stanford_jar)

    def test_stanford_jar_path_true(self):

        """Function:  test_stanford_jar_path_true

        Description:  Test if stanford_jar path check is True.

        Arguments:

        """

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_stanford_jar_false(self):

        """Function:  test_stanford_jar_false

        Description:  Test if stanford_jar check returns False.

        Arguments:

        """

        self.cfg.stanford_jar = self.err_msg7
        full_msg = self.tmp4 % self.err_msg7 + self.tmp6 % self.err_msg7

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_stanford_jar_true2(self):

        """Function:  test_stanford_jar_true2

        Description:  Test if stanford_jar check returns True.

        Arguments:

        """

        stanford_jar = self.cfg.stanford_jar

        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.stanford_jar, stanford_jar)

    def test_stanford_jar_true(self):

        """Function:  test_stanford_jar_true

        Description:  Test if stanford_jar check returns True.

        Arguments:

        """

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_lang_module_path_false(self):

        """Function:  test_lang_module_path_false

        Description:  Test if lang_module path check is False.

        Arguments:

        """

        self.cfg.lang_module = "./" + self.cfg.lang_module
        full_msg = self.tmp8 % self.cfg.lang_module

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_lang_module_path_true2(self):

        """Function:  test_lang_module_path_true2

        Description:  Test if lang_module path check is True.

        Arguments:

        """

        lang_mod = self.cfg.lang_module

        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.lang_module, lang_mod)

    def test_lang_module_path_true(self):

        """Function:  test_lang_module_path_true

        Description:  Test if lang_module path check is True.

        Arguments:

        """

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_lang_module_false(self):

        """Function:  test_lang_module_false

        Description:  Test if lang_module check returns False.

        Arguments:

        """

        self.cfg.lang_module = self.err_msg5
        full_msg = self.tmp4 % self.err_msg5 + self.tmp6 % self.err_msg5

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_lang_module_true2(self):

        """Function:  test_lang_module_true2

        Description:  Test if lang_module check returns True.

        Arguments:

        """

        lang_mod = self.cfg.lang_module

        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.lang_module, lang_mod)

    def test_lang_module_true(self):

        """Function:  test_lang_module_true

        Description:  Test if lang_module check returns True.

        Arguments:

        """

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_tmp_dir_false(self):

        """Function:  test_tmp_dir_false

        Description:  Test if tmp_dir check returns False.

        Arguments:

        """

        self.cfg.tmp_dir = self.err_msg4
        full_msg = self.tmp % self.err_msg4 + self.tmp2 % self.err_msg4 \
                   + self.tmp3 % self.err_msg4

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_tmp_dir_not_abs2(self):

        """Function:  test_tmp_dir_not_abs2

        Description:  Test when tmp_dir is not abs.

        Arguments:

        """

        sub_tmp_dir = "test/integration/rmq_metadata/tmp"
        tmp_dir = os.path.join(os.getcwd(), sub_tmp_dir)
        self.cfg.tmp_dir = sub_tmp_dir

        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.tmp_dir, tmp_dir)

    def test_tmp_dir_not_abs(self):

        """Function:  test_tmp_dir_not_abs

        Description:  Test when tmp_dir is not abs.

        Arguments:

        """

        sub_tmp_dir = "test/integration/rmq_metadata/tmp"
        self.cfg.tmp_dir = sub_tmp_dir

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_tmp_dir_true2(self):

        """Function:  test_tmp_dir_true2

        Description:  Test if tmp_dir check returns True.

        Arguments:

        """

        tmp_dir = self.cfg.tmp_dir

        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.tmp_dir, tmp_dir)

    def test_tmp_dir_true(self):

        """Function:  test_tmp_dir_true

        Description:  Test if tmp_dir check returns True.

        Arguments:

        """

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_archive_dir_false(self):

        """Function:  test_archive_dir_false

        Description:  Test if archive_dir check returns False.

        Arguments:

        """

        self.cfg.archive_dir = self.err_msg3
        full_msg = self.tmp % self.err_msg3 + self.tmp2 % self.err_msg3 \
                   + self.tmp3 % self.err_msg3


        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_archive_not_abs2(self):

        """Function:  test_archive_not_abs2

        Description:  Test when archive_dir is not abs.

        Arguments:

        """

        sub_archive_dir = "test/integration/rmq_metadata/archive"
        archive_dir = os.path.join(os.getcwd(), sub_archive_dir)
        self.cfg.archive_dir = sub_archive_dir

        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.archive_dir, archive_dir)

    def test_archive_not_abs(self):

        """Function:  test_archive_not_abs

        Description:  Test when archive_dir is not abs.

        Arguments:

        """

        sub_archive_dir = "test/integration/rmq_metadata/archive"
        self.cfg.archive_dir = sub_archive_dir

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_archive_dir_true2(self):

        """Function:  test_archive_dir_true2

        Description:  Test if archive_dir check returns True.

        Arguments:

        """

        archive_dir = self.cfg.archive_dir
        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.archive_dir, archive_dir)

    def test_archive_dir_true(self):

        """Function:  test_archive_dir_true

        Description:  Test if archive_dir check returns True.

        Arguments:

        """

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_multiple_false(self):

        """Function:  test_multiple_false

        Description:  Test if multiple checks return False.

        Arguments:

        """

        self.cfg.message_dir = self.err_msg9
        self.cfg.log_dir = self.err_msg2
        full_msg = self.tmp % self.err_msg9 + self.tmp2 % self.err_msg9 \
                   + self.tmp3 % self.err_msg9
        full_msg2 = self.tmp % self.err_msg2 + self.tmp2 % self.err_msg2 \
                    + self.tmp3 % self.err_msg2


        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg + full_msg2))

    def test_log_dir_false(self):

        """Function:  test_log_dir_false

        Description:  Test if log_dir check returns False.

        Arguments:

        """

        self.cfg.log_dir = self.err_msg2
        full_msg = self.tmp % self.err_msg2 + self.tmp2 % self.err_msg2 \
                   + self.tmp3 % self.err_msg2

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_log_dir_true2(self):

        """Function:  test_log_dir_true2

        Description:  Test if log_dir check returns True.

        Arguments:

        """

        base_name, ext_name = os.path.splitext(self.cfg.log_file)
        log_name = base_name + "_" + self.cfg.exchange_name + ext_name
        new_log_file = os.path.join(self.cfg.log_dir, log_name)

        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.log_file, new_log_file)

    def test_log_dir_true(self):

        """Function:  test_log_dir_true

        Description:  Test if log_dir check returns True.

        Arguments:

        """

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def test_message_dir_false(self):

        """Function:  test_message_dir_false

        Description:  Test if message_dir check returns False.

        Arguments:

        """

        self.cfg.message_dir = self.err_msg
        full_msg = self.tmp % self.err_msg + self.tmp2 % self.err_msg \
                   + self.tmp3 % self.err_msg

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (False, full_msg))

    def test_message_dir_true2(self):

        """Function:  test_message_dir_true2

        Description:  Test if message_dir check returns True.

        Arguments:

        """

        message_dir = self.cfg.message_dir
        cfg, _, _ = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual(cfg.message_dir, message_dir)

    def test_message_dir_true(self):

        """Function:  test_message_dir_true

        Description:  Test if message_dir check returns True.

        Arguments:

        """

        _, status, err_msg = rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status, err_msg), (True, ""))

    def tearDown(self):

        """Function:  tearDown

        Description:  Cleanup of test environment.

        Arguments:

        """

        del sys.modules["rabbitmq"]


if __name__ == "__main__":
    unittest.main()
