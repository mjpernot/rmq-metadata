# Classification (U)

"""Program:  process_message.py

    Description:  Unit testing of process_message in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/process_message.py

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
        setUp
        test_mongo_failed
        test_mongo_successful
        test_all_extract_fails
        test_two_extract_fails3
        test_two_extract_fails2
        test_two_extract_fails
        test_pdfminer_extract_fails
        test_textract_extract_fails
        test_pypdf2_extract_fails
        test_all_successful_extracts

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

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=(False, "Connection Error")))
    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_mongo_failed(self, mock_pypdf2, mock_textract, mock_pdfminer):

        """Function:  test_mongo_failed

        Description:  Test with failed Mongo insert.

        Arguments:

        """

        mock_pypdf2.return_value = (True, self.final_data)
        mock_textract.return_value = (True, self.final_data)
        mock_pdfminer.return_value = (True, self.final_data)

        self.assertFalse(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    @mock.patch("rmq_metadata.get_pdfminer_data")
    @mock.patch("rmq_metadata.get_textract_data")
    @mock.patch("rmq_metadata.get_pypdf2_data")
    def test_mongo_successful(self, mock_pypdf2, mock_textract, mock_pdfminer):

        """Function:  test_mongo_successful

        Description:  Test with successful Mongo insert.

        Arguments:

        """

        mock_pypdf2.return_value = (True, self.final_data)
        mock_textract.return_value = (True, self.final_data)
        mock_pdfminer.return_value = (True, self.final_data)

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

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

        self.assertFalse(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
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

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
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

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
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

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
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

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
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

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
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

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))

    @mock.patch("rmq_metadata.create_metadata", mock.Mock(return_value="data"))
    @mock.patch("rmq_metadata.gen_libs.mv_file2", mock.Mock(return_value=True))
    @mock.patch("rmq_metadata.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
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

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.f_name, self.logger))


if __name__ == "__main__":
    unittest.main()
