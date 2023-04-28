# Classification (U)

"""Program:  get_textract_data.py

    Description:  Unit testing of get_textract_data in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/get_textract_data.py

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
        log_warn
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
            (input) data

        """

        self.data = data

    def log_warn(self, data):

        """Method:  log_warn

        Description:  log_warn method.

        Arguments:

        """

        self.data = data

    def log_err(self, data):

        """Method:  log_err

        Description:  log_err method.

        Arguments:

        """

        self.data = data


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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_extract_failure
        test_extract_successful
        test_categorized_text2
        test_categorized_text
        test_confidence2
        test_confidence
        test_get_textract_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.f_name = "Filename.pdf"
        self.text = "This is extracted text"
        self.data = {"confidence": 1.0, "encoding": "utf-8"}
        self.data2 = {"confidence": 0.9, "encoding": "utf-8"}
        self.tokens = ["Tokens Strings", "Another token string"]
        self.categorized_text = [("Token", "O"), ("Strings", "O")]
        self.categorized_text2 = []
        self.final_data = [("Place", "LOCATION")]
        self.results = [("Place", "LOCATION")]
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")

    @mock.patch("rmq_metadata.extract_pdf")
    def test_extract_failure(self, mock_extract):

        """Function:  test_extract_failure

        Description:  Test with failed extraction of data.

        Arguments:

        """

        mock_extract.return_value = (False, "")

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            (False, []))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.chardet.detect")
    @mock.patch("rmq_metadata.extract_pdf")
    def test_extract_successful(self, mock_extract, mock_chardet, mock_token,
                                mock_find, mock_sum):

        """Function:  test_extract_successful

        Description:  Test with successful extraction of data.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_chardet.return_value = self.data
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            (True, self.results))

    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.chardet.detect")
    @mock.patch("rmq_metadata.extract_pdf")
    def test_categorized_text2(self, mock_extract, mock_chardet, mock_token,
                               mock_find):

        """Function:  test_categorized_text2

        Description:  Test with no categorized text.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_chardet.return_value = self.data
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text2

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            (True, []))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.chardet.detect")
    @mock.patch("rmq_metadata.extract_pdf")
    def test_categorized_text(self, mock_extract, mock_chardet, mock_token,
                              mock_find, mock_sum):

        """Function:  test_categorized_text

        Description:  Test with categorized text.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_chardet.return_value = self.data
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            (True, self.results))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.chardet.detect")
    @mock.patch("rmq_metadata.extract_pdf")
    def test_confidence2(self, mock_extract, mock_chardet, mock_token,
                         mock_find, mock_sum):

        """Function:  test_confidence2

        Description:  Test with confidence not equal to 1.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_chardet.return_value = self.data2
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            (True, self.results))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.chardet.detect")
    @mock.patch("rmq_metadata.extract_pdf")
    def test_confidence(self, mock_extract, mock_chardet, mock_token,
                        mock_find, mock_sum):

        """Function:  test_confidence

        Description:  Test with confidence equal to 1.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_chardet.return_value = self.data
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            (True, self.results))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.chardet.detect")
    @mock.patch("rmq_metadata.extract_pdf")
    def test_get_textract_data(self, mock_extract, mock_chardet, mock_token,
                               mock_find, mock_sum):

        """Function:  test_get_textract_data

        Description:  Test with extracting data.

        Arguments:

        """

        mock_extract.return_value = (True, self.text)
        mock_chardet.return_value = self.data
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            (True, self.results))


if __name__ == "__main__":
    unittest.main()
