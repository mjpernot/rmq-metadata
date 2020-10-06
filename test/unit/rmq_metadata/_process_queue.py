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
        log_err -> log_err method.

    """

    def __init__(self, job_name, job_log, log_type, log_format, log_time):

        """Method:  __init__

        Description:  Initialization instance of the class.

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

    def log_err(self, data):

        """Method:  log_err

        Description:  log_err method.

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
        self.mongo = None


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_all_extract_fails -> Test with all extracts fails.
        test_two_extract_fails3 -> Test with two extracts fails.
        test_two_extract_fails2 -> Test with two extracts fails.
        test_two_extract_fails -> Test with two extracts fails.
        test_pdfminer_extract_fails -> Test with pdfminer extract fails.
        test_textract_extract_fails -> Test with textract extract fails.
        test_pypdf2_extract_fails -> Test with pypdf2 extract fails.
        test_all_successful_extracts -> Test with all successful extracts.

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
        self.f_name = "/working/path/Filename.pdf"
        self.final_data = ["List", "of", "a", "data"]

    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_all_extract_fails(self, mock_pypdf2, mock_textract,
                               mock_pdfminer):

        """Function:  test_all_extract_fails

        Description:  Test with all extracts fails.

        Arguments:

        """

        mock_pypdf2.return_value = (False, [])
        mock_textract.return_value = (False, [])
        mock_pdfminer.return_value = (False, [])

        self.assertFalse(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_two_extract_fails3(self, mock_pypdf2, mock_textract,
                                mock_pdfminer):

        """Function:  test_two_extract_fails3

        Description:  Test with two extracts fails.

        Arguments:

        """

        mock_pypdf2.return_value = (False, [])
        mock_textract.return_value = (False, [])
        mock_pdfminer.return_value = (True, self.final_data)

        self.assertTrue(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_two_extract_fails2(self, mock_pypdf2, mock_textract,
                                mock_pdfminer):

        """Function:  test_two_extract_fails2

        Description:  Test with two extracts fails.

        Arguments:

        """

        mock_pypdf2.return_value = (False, [])
        mock_textract.return_value = (True, self.final_data)
        mock_pdfminer.return_value = (False, [])

        self.assertTrue(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_two_extract_fails(self, mock_pypdf2, mock_textract,
                               mock_pdfminer):

        """Function:  test_two_extract_fails

        Description:  Test with two extracts fails.

        Arguments:

        """

        mock_pypdf2.return_value = (True, self.final_data)
        mock_textract.return_value = (False, [])
        mock_pdfminer.return_value = (False, [])

        self.assertTrue(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_pdfminer_extract_fails(self, mock_pypdf2, mock_textract,
                                    mock_pdfminer):

        """Function:  test_pdfminer_extract_fails

        Description:  Test with pdfminer extract fails.

        Arguments:

        """

        mock_pypdf2.return_value = (True, self.final_data)
        mock_textract.return_value = (True, self.final_data)
        mock_pdfminer.return_value = (False, [])

        self.assertTrue(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_textract_extract_fails(self, mock_pypdf2, mock_textract,
                                    mock_pdfminer):

        """Function:  test_textract_extract_fails

        Description:  Test with textract extract fails.

        Arguments:

        """

        mock_pypdf2.return_value = (True, self.final_data)
        mock_textract.return_value = (False, [])
        mock_pdfminer.return_value = (True, self.final_data)

        self.assertTrue(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_pypdf2_extract_fails(self, mock_pypdf2, mock_textract,
                                  mock_pdfminer):

        """Function:  test_pypdf2_extract_fails

        Description:  Test with pypdf2 extract fails.

        Arguments:

        """

        mock_pypdf2.return_value = (False, [])
        mock_textract.return_value = (True, self.final_data)
        mock_pdfminer.return_value = (True, self.final_data)

        self.assertTrue(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_all_successful_extracts(self, mock_pypdf2, mock_textract,
                                     mock_pdfminer):

        """Function:  test_all_successful_extracts

        Description:  Test with all successful extracts.

        Arguments:

        """

        mock_pypdf2.return_value = (True, self.final_data)
        mock_textract.return_value = (True, self.final_data)
        mock_pdfminer.return_value = (True, self.final_data)

        self.assertTrue(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))


if __name__ == "__main__":
    unittest.main()
