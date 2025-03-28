# Classification (U)

"""Program:  process_msg.py

    Description:  Unit testing of process_msg in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/process_msg.py

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
import rmq_metadata                             # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class RabbitMQCon():                                    # pylint:disable=R0903

    """Class:  RabbitMQCon

    Description:  Class which is a representation of
        rabbitmq_class.RabbitMQCon class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.exchange = "Exchange_Name"


class Logger():                                         # pylint:disable=R0903

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__
        log_info

    """

    def __init__(                                       # pylint:disable=R0913
            self, job_name, job_log, log_type, log_format, log_time):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.job_name = job_name
        self.job_log = job_log
        self.log_type = log_type
        self.log_format = log_format
        self.log_time = log_time
        self.data = None

    def log_info(self, data):

        """Method:  log_info

        Description:  log_info method.

        Arguments:

        """

        self.data = data


class MethodTest():                                     # pylint:disable=R0903

    """Class:  MethodTest

    Description:  Class which is a representation of a method module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.routing_key = "MY_ROUTING_KEY"


class CfgTest():                                        # pylint:disable=R0903

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
        self.archive_dir = "/dir/archive_path"
        self.queue_list = [
            {"queue": "rmq_metadata_unit_test",
             "routing_key": "MY_ROUTING_KEY",
             "directory": "/dir/path",
             "prename": "Pre-filename",
             "postname": "Post-filename",
             "mode": "w",
             "ext": "pdf",
             "stype": "encoded",
             "archive": False}]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_multiple_queue_archive
        test_multiple_queue_found
        test_archive_body
        test_queue_found
        test_queue_not_found
        test_no_queue_list

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.rmq = RabbitMQCon()
        self.body = "ThekljdsfkjsfdJVBERi0xLjQKJeLjz9MKMTAgMCBvYmoKPDwKL0EgP"
        self.method = MethodTest()
        self.cfg = CfgTest()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.queue = {"queue": "rmq_metadata_unit_test2",
                      "routing_key": "MY_ROUTING_KEY2",
                      "directory": "/dir/path2", "prename": "Pre-filename",
                      "postname": "Post-filename", "mode": "w", "ext": "pdf",
                      "stype": "encoded", "archive": False}
        self.queue2 = {"queue": "rmq_metadata_unit_test3",
                       "routing_key": "MY_ROUTING_KEY3",
                       "directory": "/dir/path3", "prename": "Pre-filename",
                       "postname": "Post-filename", "mode": "w", "ext": "pdf",
                       "stype": "encoded", "archive": True}

    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.convert_data", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.non_proc_msg", mock.Mock(return_value=True))
    def test_multiple_queue_archive(self):

        """Function:  test_multiple_queue_archive

        Description:  Test with archiving message body in multiple queues.

        Arguments:

        """

        self.cfg.queue_list.append(self.queue2)
        self.method.routing_key = "MY_ROUTING_KEY3"

        self.assertFalse(
            rmq_metadata.process_msg(
                self.rmq, self.logger, self.cfg, self.method, self.body))

    @mock.patch("rmq_metadata.convert_data", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.non_proc_msg", mock.Mock(return_value=True))
    def test_multiple_queue_found(self):

        """Function:  test_multiple_queue_found

        Description:  Test with multiple queues found in queue_list.

        Arguments:

        """

        self.cfg.queue_list.append(self.queue)
        self.method.routing_key = "MY_ROUTING_KEY2"

        self.assertFalse(
            rmq_metadata.process_msg(
                self.rmq, self.logger, self.cfg, self.method, self.body))

    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.convert_data", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.non_proc_msg", mock.Mock(return_value=True))
    def test_archive_body(self):

        """Function:  test_archive_body

        Description:  Test with archiving message body.

        Arguments:

        """

        self.cfg.queue_list[0]["archive"] = True

        self.assertFalse(
            rmq_metadata.process_msg(
                self.rmq, self.logger, self.cfg, self.method, self.body))

    @mock.patch("rmq_metadata.convert_data", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.non_proc_msg", mock.Mock(return_value=True))
    def test_queue_found(self):

        """Function:  test_queue_found

        Description:  Test with queue found in queue_list.

        Arguments:

        """

        self.assertFalse(
            rmq_metadata.process_msg(
                self.rmq, self.logger, self.cfg, self.method, self.body))

    @mock.patch("rmq_metadata.non_proc_msg", mock.Mock(return_value=True))
    def test_queue_not_found(self):

        """Function:  test_queue_not_found

        Description:  Test with no queue found in queue_list.

        Arguments:

        """

        self.cfg.queue_list[0]["routing_key"] = "NotMyKey"

        self.assertFalse(
            rmq_metadata.process_msg(
                self.rmq, self.logger, self.cfg, self.method, self.body))

    @mock.patch("rmq_metadata.non_proc_msg", mock.Mock(return_value=True))
    def test_no_queue_list(self):

        """Function:  test_no_queue_list

        Description:  Test with an empty queue list.

        Arguments:

        """

        self.cfg.queue_list = []

        self.assertFalse(
            rmq_metadata.process_msg(
                self.rmq, self.logger, self.cfg, self.method, self.body))


if __name__ == "__main__":
    unittest.main()
