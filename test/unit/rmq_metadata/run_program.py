#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/run_program.py

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


def monitor_queue(cfg, log):

    """Function Stub:  monitor_queue

    Description:  This is a function stub for rmq_metadata.monitor_queue

    Arguments:

    """

    status = True

    if cfg and log:
        status = True

    return status


class CfgTest2(object):

    """Class:  CfgTest2

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.host = "IP_Address"
        self.port = 27017
        self.name = "HostName"
        self.conf_file = None
        self.auth = True
        self.dbs = "Database_Name"
        self.tbl = "Table_Name"
        self.repset = None
        self.repset_hosts = None
        self.db_auth = None


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

        self.user = "USER"
        self.japd = ""
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
        self.lang_module = \
            "DIRECTORY_PATH/classifiers/english.all.3class.distsim.crf.ser.gz"
        self.stanford_jar = "DIRECTORY_PATH/stanford-ner.jar"
        self.encoding = "utf-8"
        self.token_types = ["LOCATION", "PERSON", "ORGANIZATION"]
        self.textract_codes = ["utf-8", "ascii", "iso-8859-1"]
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
        self.mongo_cfg = "mongo"
        self.mongo = None


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) cmdline
            (input) flavor

        """

        self.cmdline = cmdline
        self.flavor = flavor


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_flavor_id2
        test_flavor_id
        test_status_false
        test_status_true
        test_func_call
        test_raise_exception
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.mongo_cfg = CfgTest2()
        self.proglock = ProgramLock(["cmdline"], "FlavorID")
        self.args = {"-c": "config_file", "-d": "config_dir", "-M": True}
        self.args2 = {"-c": "config_file", "-d": "config_dir", "-M": True,
                      "-y": "flavorid"}
        self.func_dict = {"-M": monitor_queue}

    @mock.patch("rmq_metadata.monitor_queue")
    @mock.patch("rmq_metadata.validate_create_settings")
    @mock.patch("rmq_metadata.gen_libs.load_module")
    @mock.patch("rmq_metadata.gen_class")
    def test_flavor_id2(self, mock_class, mock_load, mock_valid, mock_func):

        """Function:  test_flavor_id2

        Description:  Test with passed flavor id argument.

        Arguments:

        """

        mock_class.Logger.return_value = rmq_metadata.gen_class.Logger
        mock_load.side_effect = [self.cfg, self.mongo_cfg]
        mock_valid.return_value = (self.cfg, True, "")
        mock_class.Logger.log_close.return_value = True
        mock_class.ProgramLock.return_value = self.proglock
        mock_func.return_value = True

        self.assertFalse(rmq_metadata.run_program(self.args2, self.func_dict))

    @mock.patch("rmq_metadata.monitor_queue")
    @mock.patch("rmq_metadata.validate_create_settings")
    @mock.patch("rmq_metadata.gen_libs.load_module")
    @mock.patch("rmq_metadata.gen_class")
    def test_flavor_id(self, mock_class, mock_load, mock_valid, mock_func):

        """Function:  test_flavor_id

        Description:  Test with default setting.

        Arguments:

        """

        mock_class.Logger.return_value = rmq_metadata.gen_class.Logger
        mock_load.side_effect = [self.cfg, self.mongo_cfg]
        mock_valid.return_value = (self.cfg, True, "")
        mock_class.Logger.log_close.return_value = True
        mock_class.ProgramLock.return_value = self.proglock
        mock_func.return_value = True

        self.assertFalse(rmq_metadata.run_program(self.args, self.func_dict))

    @mock.patch("rmq_metadata.validate_create_settings")
    @mock.patch("rmq_metadata.gen_libs.load_module")
    @mock.patch("rmq_metadata.gen_class.Logger")
    def test_status_false(self, mock_log, mock_load, mock_valid):

        """Function:  test_status_false

        Description:  Test run_program function with status is False.

        Arguments:

        """

        mock_log.return_value = True
        mock_load.side_effect = [self.cfg, self.mongo_cfg]
        mock_valid.return_value = (self.cfg, False, "Failed to load cfg")

        with gen_libs.no_std_out():
            self.assertFalse(rmq_metadata.run_program(self.args,
                                                      self.func_dict))

    @mock.patch("rmq_metadata.validate_create_settings")
    @mock.patch("rmq_metadata.gen_libs.load_module")
    @mock.patch("rmq_metadata.gen_class.Logger")
    def test_status_true(self, mock_log, mock_load, mock_valid):

        """Function:  test_status_true

        Description:  Test run_program function with status is True.

        Arguments:

        """

        mock_log.return_value = rmq_metadata.gen_class.Logger
        mock_load.side_effect = [self.cfg, self.mongo_cfg]
        mock_valid.return_value = (self.cfg, True, "")
        mock_log.log_close.return_value = True

        # Remove to skip "for" loop.
        self.args.pop("-M")

        self.assertFalse(rmq_metadata.run_program(self.args, self.func_dict))

    @mock.patch("rmq_metadata.monitor_queue")
    @mock.patch("rmq_metadata.validate_create_settings")
    @mock.patch("rmq_metadata.gen_libs.load_module")
    @mock.patch("rmq_metadata.gen_class")
    def test_func_call(self, mock_class, mock_load, mock_valid, mock_func):

        """Function:  test_func_call

        Description:  Test run_program function with call to function.

        Arguments:

        """

        mock_class.Logger.return_value = rmq_metadata.gen_class.Logger
        mock_load.side_effect = [self.cfg, self.mongo_cfg]
        mock_valid.return_value = (self.cfg, True, "")
        mock_class.Logger.log_close.return_value = True
        mock_class.ProgramLock.return_value = self.proglock
        mock_func.return_value = True

        self.assertFalse(rmq_metadata.run_program(self.args, self.func_dict))

    @mock.patch("rmq_metadata.gen_class.Logger")
    @mock.patch("rmq_metadata.validate_create_settings")
    @mock.patch("rmq_metadata.gen_libs.load_module")
    @mock.patch("rmq_metadata.gen_class.ProgramLock")
    def test_raise_exception(self, mock_lock, mock_load, mock_valid, mock_log):

        """Function:  test_raise_exception

        Description:  Test run_program function with raising the exception.

        Arguments:

        """

        mock_lock.side_effect = rmq_metadata.gen_class.SingleInstanceException
        mock_log.return_value = rmq_metadata.gen_class.Logger
        mock_log.log_info.return_value = True
        mock_log.log_close.return_value = True
        mock_load.side_effect = [self.cfg, self.mongo_cfg]
        mock_valid.return_value = (self.cfg, True, "")

        self.assertFalse(rmq_metadata.run_program(self.args, self.func_dict))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        self.cfg = None


if __name__ == "__main__":
    unittest.main()
