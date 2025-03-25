# Classification (U)

"""Program:  get_pdfminer_data.py

    Description:  Unit testing of get_pdfminer_data in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/get_pdfminer_data.py

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


class Logger():

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__
        log_info
        log_err

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

    def log_err(self, data):

        """Method:  log_err

        Description:  log_err method.

        Arguments:

        """

        self.data = data


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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_extract_failure
        test_extract_success
        test_categorized_text2
        test_categorized_text
        test_get_pdfminer_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.f_name = "Filename.pdf"
        self.text = "This is extracted text"
        self.tokens = ["Tokens Strings", "Another token string"]
        self.categorized_text = [("Token", "O"), ("Strings", "O")]
        self.categorized_text2 = []
        self.final_data = [("Place", "LOCATION")]
        self.results = [("Place", "LOCATION")]
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.pdf_to_string")
    def test_extract_failure(self, mock_extract, mock_token, mock_find,
                             mock_sum):

        """Function:  test_extract_failure

        Description:  Test with failure of extraction.

        Arguments:

        """

        mock_extract.return_value = (False, "")
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_pdfminer_data(self.f_name, self.cfg, self.logger),
            (False, []))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.pdf_to_string")
    def test_extract_success(self, mock_extract, mock_token, mock_find,
                             mock_sum):

        """Function:  test_extract_success

        Description:  Test with successful extraction.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_pdfminer_data(self.f_name, self.cfg, self.logger),
            (True, self.results))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.pdf_to_string")
    def test_categorized_text2(self, mock_extract, mock_token, mock_find,
                               mock_sum):

        """Function:  test_categorized_text2

        Description:  Test with no categorized text.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text2
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_pdfminer_data(self.f_name, self.cfg, self.logger),
            (True, []))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.pdf_to_string")
    def test_categorized_text(self, mock_extract, mock_token, mock_find,
                              mock_sum):

        """Function:  test_categorized_text

        Description:  Test with categorized text.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_pdfminer_data(self.f_name, self.cfg, self.logger),
            (True, self.results))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.pdf_to_string")
    def test_get_pdfminer_data(self, mock_extract, mock_token, mock_find,
                               mock_sum):

        """Function:  test_get_pdfminer_data

        Description:  Test with extracting data.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_pdfminer_data(self.f_name, self.cfg, self.logger),
            (True, self.results))


if __name__ == "__main__":
    unittest.main()
