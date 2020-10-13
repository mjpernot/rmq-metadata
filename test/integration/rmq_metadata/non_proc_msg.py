#!/usr/bin/python
# Classification (U)

"""Program:  non_proc_msg.py

    Description:  Integration testing of non_proc_msg in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/non_proc_msg.py

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
import lib.gen_class as gen_class
import lib.gen_libs as gen_libs
import rabbit_lib.rabbitmq_class as rabbitmq_class
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_write_file -> Test with writing body to file.
        test_to_empty_line -> Test for empty to line.
        test_to_line -> Test for valid to line.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        integration_dir = "test/integration/rmq_metadata"
        base_path = os.path.join(os.getcwd(), integration_dir)
        config_dir = os.path.join(base_path, "config")
        self.cfg = gen_libs.load_module("rabbitmq", config_dir)
        log_dir = os.path.join(base_path, "logs")
        self.log_file = os.path.join(log_dir, "rmq_metadata.log")
        self.msg_dir = os.path.join(base_path, "message_dir")
        self.filter_name = self.cfg.exchange_name + "_" \
                           + self.cfg.queue_list[0]["routing_key"] + "_*"
        self.logger = gen_class.Logger(
            self.log_file, self.log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")

        self.rmq = rabbitmq_class.RabbitMQCon(
            self.cfg.user, self.cfg.japd, self.cfg.host, self.cfg.port,
            exchange_name=self.cfg.exchange_name,
            exchange_type=self.cfg.exchange_type,
            queue_name=self.cfg.queue_list[0]["queue"],
            routing_key=self.cfg.queue_list[0]["routing_key"],
            x_durable=self.cfg.x_durable, q_durable=self.cfg.q_durable,
            auto_delete=self.cfg.auto_delete)

        self.r_key = self.cfg.queue_list[0]["routing_key"]
        self.data = "Body of message"
        self.subj = "Test_Subject"

    def test_write_file(self):

        """Function:  test_write_file

        Description:  Test with writing body to file.

        Arguments:

        """

        rmq_metadata.non_proc_msg(self.rmq, self.logger, self.cfg, self.data,
                                  self.subj, self.r_key)
        f_list = gen_libs.list_filter_files(self.msg_dir, self.filter_name)

        self.assertTrue(f_list and len(f_list) == 1
                        and os.path.isfile(f_list[0]))

    def test_empty_to_line(self):

        """Function:  test_empty_to_line

        Description:  Test non_proc_msg function with empty to line.

        Arguments:

        """

        rmq_metadata.non_proc_msg(self.rmq, self.logger, self.cfg, self.data,
                                  self.subj, self.r_key)
        f_list = gen_libs.list_filter_files(self.msg_dir, self.filter_name)

        self.assertTrue(f_list and len(f_list) == 1
                        and os.path.isfile(f_list[0]))

    @mock.patch("rmq_metadata.gen_class.Mail")
    def test_to_line(self, mock_mail):

        """Function:  test_to_line

        Description:  Test non_proc_msg function with valid to line.

        Arguments:

        """

        self.cfg.to_line = "Test_Email@email.domain"

        mock_mail.send_mail.return_value = True

        rmq_metadata.non_proc_msg(self.rmq, self.logger, self.cfg, self.data,
                                  self.subj, self.r_key)
        f_list = gen_libs.list_filter_files(self.msg_dir, self.filter_name)

        self.assertTrue(f_list and len(f_list) == 1
                        and os.path.isfile(f_list[0]))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        del sys.modules["rabbitmq"]

        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

        for item in gen_libs.list_filter_files(self.msg_dir, self.filter_name):
            os.remove(item)

if __name__ == "__main__":
    unittest.main()
