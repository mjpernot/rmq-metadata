#!/usr/bin/python
# Classification (U)

"""Program:  convert_data.py

    Description:  Unit testing of convert_data in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/convert_data.py

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


class RabbitMQCon(object):

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


class Logger(object):

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__
        log_info
        log_err

    """

    def __init__(self, job_name, job_log, log_type, log_format, log_time):

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

    def log_err(self, data):

        """Method:  log_err

        Description:  log_err method.

        Arguments:

        """

        self.data = data


class MethodTest(object):

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

        self.routing_key = "ROUTING_KEY"


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
        self.tmp_dir = "./test/unit/rmq_metadata/testfiles"
        self.queue_list = [
            {"queue": "rmq_metadata_unit_test",
             "routing_key": "ROUTING_KEY",
             "directory": "/dir/path",
             "prename": "",
             "postname": "",
             "mode": "w",
             "ext": "pdf",
             "stype": "encoded",
             "archive": False}]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_extract_fails
        test_prename_postname_ext
        test_prename_postname
        test_no_prename
        test_prename_change
        test_prename_default
        test_no_postname
        test_postname_change
        test_postname_default
        test_empty_ext
        test_no_ext
        test_ext_change
        test_ext_default
        test_file_not_encoded -> Test with file not encoded
        test_file_encoded
        test_default_name
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.tmpdir = "./test/unit/rmq_metadata/testfiles"
        self.t_file = os.path.join(self.tmpdir, "t_file.txt")
        self.f_name = os.path.join(self.tmpdir, "f_file.txt")

        self.rmq = RabbitMQCon()
        self.body = "ThekljdsfkjsfdJVBERi0xLjQKJeLjz9MKMTAgMCBvYmoKPDwKL0EgP"
        self.method = MethodTest()
        self.cfg = CfgTest()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")

    @mock.patch("rmq_metadata.non_proc_msg", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=False))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_extract_fails(self, mock_path):

        """Function:  test_extract_fails

        Description:  Test with extraction fails.

        Arguments:

        """

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_prename_postname_ext(self, mock_path):

        """Function:  test_prename_postname_ext

        Description:  Test with prename, postname, and ext.

        Arguments:

        """

        self.cfg.queue_list[0]["prename"] = "pre_name"
        self.cfg.queue_list[0]["postname"] = "post_name"
        self.cfg.queue_list[0]["ext"] = "txt"

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_prename_postname(self, mock_path):

        """Function:  test_prename_postname

        Description:  Test with change to prename and postname.

        Arguments:

        """

        self.cfg.queue_list[0]["prename"] = "pre_name"
        self.cfg.queue_list[0]["postname"] = "post_name"

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_no_prename(self, mock_path):

        """Function:  test_no_prename

        Description:  Test with no prename set.

        Arguments:

        """

        self.cfg.queue_list[0]["prename"] = None

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_prename_change(self, mock_path):

        """Function:  test_prename_change

        Description:  Test with change to default prename.

        Arguments:

        """

        self.cfg.queue_list[0]["prename"] = "pre_name"

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_prename_default(self, mock_path):

        """Function:  test_prename_default

        Description:  Test with default prename.

        Arguments:

        """

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_no_postname(self, mock_path):

        """Function:  test_no_postname

        Description:  Test with no postname set.

        Arguments:

        """

        self.cfg.queue_list[0]["postname"] = None

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_postname_change(self, mock_path):

        """Function:  test_postname_change

        Description:  Test with change to default postname.

        Arguments:

        """

        self.cfg.queue_list[0]["postname"] = "post_name"

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_postname_default(self, mock_path):

        """Function:  test_postname_default

        Description:  Test with default postname.

        Arguments:

        """

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_empty_ext(self, mock_path):

        """Function:  test_empty_ext

        Description:  Test with empty extension set.

        Arguments:

        """

        self.cfg.queue_list[0]["ext"] = ""

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_no_ext(self, mock_path):

        """Function:  test_no_ext

        Description:  Test with no extension set.

        Arguments:

        """

        self.cfg.queue_list[0]["ext"] = None

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_ext_change(self, mock_path):

        """Function:  test_ext_change

        Description:  Test with change to default extension.

        Arguments:

        """

        self.cfg.queue_list[0]["ext"] = "txt"

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_ext_default(self, mock_path):

        """Function:  test_ext_default

        Description:  Test with default extension.

        Arguments:

        """

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.rename_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_file_not_encoded(self, mock_path):

        """Function:  test_file_not_encoded

        Description:  Test with file not encoded.

        Arguments:

        """

        self.cfg.queue_list[0]["stype"] = "not_encoded"

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_file_encoded(self, mock_path):

        """Function:  test_file_encoded

        Description:  Test with file encoded.

        Arguments:

        """

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    @mock.patch("rmq_metadata._process_queue", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.base64.decode", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.os.path")
    def test_default_name(self, mock_path):

        """Function:  test_default_name

        Description:  Test for default file name.

        Arguments:

        """

        mock_path.join.side_effect = [self.t_file, self.f_name]

        self.assertFalse(rmq_metadata.convert_data(
            self.rmq, self.logger, self.cfg, self.cfg.queue_list[0],
            self.body, self.method.routing_key))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        if os.path.isfile(self.f_name):
            os.remove(self.f_name)


if __name__ == "__main__":
    unittest.main()
