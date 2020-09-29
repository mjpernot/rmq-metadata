#!/usr/bin/python
# Classification (U)

"""Program:  _process_queue.py

    Description:  Unit testing of _process_queue in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/_process_queue.py

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


class Logger(object):

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__ -> Initialize configuration environment.
        log_info -> log_info method.

    """

    def __init__(self, job_name, job_log, log_type, log_format, log_time):

        """Method:  __init__

        Description:  Initialization instance of the IsseGuard class.

        Arguments:
            (input) job_name -> Instance name.
            (input) job_log -> Log name.
            (input) log_type -> Log type.
            (input) log_format -> Log format.
            (input) log_time -> Time format.

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
            (input) data -> Log entry.

        """

        self.data = data


class CfgTest2(object):

    """Class:  CfgTest2

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__ -> Initialize configuration environment.

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
        self.tmp_dir = "./test/unit/rmq_metadata/testfiles"
        self.lang_module = \
            "DIRECTORY_PATH/classifiers/english.all.3class.distsim.crf.ser.gz"
        self.stanford_jar = "DIRECTORY_PATH/stanford-ner.jar"
        self.encoding = "utf-8"
        self.token_types = ["LOCATION", "PERSON", "ORGANIZATION"]
        self.textract_codes = ["utf-8", "ascii", "iso-8859-1"]
        self.queue_list = [
            {"queue": "rmq_2_isse_unit_test",
             "routing_key": "ROUTING_KEY",
             "directory": "/dir/path",
             "prename": "",
             "postname": "",
             "mode": "w",
             "ext": "pdf",
             "stype": "encoded",
             "archive": False}]
        self.mongo = None


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_process_queue -> Test the _test_process_queue function.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.cfg.mongo = CfgTest2()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.r_key = "ROUTING_KEY"
        self.body = "ThekljdsfkjsfdJVBERi0xLjQKJeLjz9MKMTAgMCBvYmoKPDwKL0EgP"
        self.f_name = "/working/path/Filename.pdf"

    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.get_textract_data",
                mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.get_pypdf2_data", mock.Mock(return_value="data"))
    def test_process_queue(self):

        """Function:  test_process_queue

        Description:  Test the _test_process_queue function.

        Arguments:

        """

        self.assertFalse(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.body, self.r_key, self.cfg,
            self.f_name, self.logger))


if __name__ == "__main__":
    unittest.main()
