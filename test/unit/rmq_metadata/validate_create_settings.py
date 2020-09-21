#!/usr/bin/python
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
        test_multi_queues_two_fail -> Test with multi queues and two failure.
        test_multi_queues_one_fail -> Test with multi queues and one failure.
        test_multiple_queues -> Test with multiple queues.
        test_multiple_false2 -> Test if multiple checks return False.
        test_multiple_false -> Test if multiple checks return False.
        test_sysmon_dir_false -> Test if sysmon_dir check returns False.
        test_sysmon_dir_true -> Test if sysmon_dir check returns True.
        test_log_dir_false -> Test if log_dir check returns False.
        test_log_dir_true -> Test if log_dir check returns True.
        test_message_dir_false -> Test if message_dir check returns False.
        test_message_dir_true -> Test if message_dir check returns True.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.host = "HOSTNAME"
                self.exchange_name = "rmq_2_isse_unit_test"
                self.to_line = None
                self.port = 5672
                self.exchange_type = "direct"
                self.x_durable = True
                self.q_durable = True
                self.auto_delete = False
                self.message_dir = "message_dir"
                self.log_dir = "logs"
                self.log_file = "rmq_2_isse.log"
                self.queue_list = [
                    {"queue": "rmq_2_isse_unit_test",
                     "routing_key": "ROUTING_KEY",
                     "directory": "/SYSMON_DIR_PATH"}]

        self.cfg = CfgTest()
        self.cfg2 = CfgTest()
        self.cfg2.queue_list.append({
            "queue": "rmq_2_isse_unit_test",
            "routing_key": "ROUTING_KEY",
            "directory": "/DIR_PATH"})
        self.base_dir = "/BASE_DIR_PATH"
        self.err_msg1 = "Missing Message Dir "
        self.err_msg2 = "Missing Log Dir "
        self.err_msg3 = "Missing Sysmon Dir "
        self.err_msg4 = "Error Queue Dir"
        base_name, ext_name = os.path.splitext(self.cfg.log_file)
        self.log_name = \
            base_name + "_" + self.cfg.exchange_name + "_" + ext_name

    @mock.patch("rmq_metadata.gen_libs")
    def test_multi_queues_two_fail(self, mock_lib):

        """Function:  test_multi_queues_two_fail

        Description:  Test with multi queues and two failure.

        Arguments:

        """

        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (False, self.err_msg4),
            (False, self.err_msg4)]
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

        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (False, self.err_msg4)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg2)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg4))

    @mock.patch("rmq_metadata.gen_libs")
    def test_multiple_queues(self, mock_lib):

        """Function:  test_multiple_queues

        Description:  Test with multiple queues.

        Arguments:

        """

        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None), (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_multiple_false2(self, mock_lib):

        """Function:  test_multiple_false

        Description:  Test if multiple checks return False.

        Arguments:

        """

        mock_lib.chk_crt_dir.side_effect = [(False, self.err_msg1),
                                            (False, self.err_msg2),
                                            (False, self.err_msg3)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg),
                         (False,
                          self.err_msg1 + self.err_msg2 + self.err_msg3))

    @mock.patch("rmq_metadata.gen_libs")
    def test_multiple_false(self, mock_lib):

        """Function:  test_multiple_false

        Description:  Test if multiple checks return False.

        Arguments:

        """

        mock_lib.chk_crt_dir.side_effect = [(False, self.err_msg1),
                                            (False, self.err_msg2),
                                            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg),
                         (False, self.err_msg1 + self.err_msg2))

    @mock.patch("rmq_metadata.gen_libs")
    def test_sysmon_dir_false(self, mock_lib):

        """Function:  test_sysmon_dir_false

        Description:  Test if sysmon_dir check returns False.

        Arguments:

        """

        mock_lib.chk_crt_dir.side_effect = [(True, None),
                                            (False, self.err_msg3),
                                            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg3))

    @mock.patch("rmq_metadata.gen_libs")
    def test_sysmon_dir_true(self, mock_lib):

        """Function:  test_sysmon_dir_true

        Description:  Test if sysmon_dir check returns True.

        Arguments:

        """

        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    @mock.patch("rmq_metadata.gen_libs")
    def test_log_dir_false(self, mock_lib):

        """Function:  test_log_dir_false

        Description:  Test if log_dir check returns False.

        Arguments:

        """

        mock_lib.chk_crt_dir.side_effect = [(True, None),
                                            (False, self.err_msg2),
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

        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
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

        mock_lib.chk_crt_dir.side_effect = [(False, self.err_msg1),
                                            (True, None), (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (False, self.err_msg1))

    @mock.patch("rmq_metadata.gen_libs")
    def test_message_dir_true(self, mock_lib):

        """Function:  test_message_dir_true

        Description:  Test if message_dir check returns True.

        Arguments:

        """

        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None)]
        _, status_flag, err_msg = \
            rmq_metadata.validate_create_settings(self.cfg)

        self.assertEqual((status_flag, err_msg), (True, ""))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        pass


if __name__ == "__main__":
    unittest.main()
