#!/usr/bin/python
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
        log_warn -> log_warn method.

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

    def log_warn(self, data):

        """Method:  log_warn

        Description:  log_warn method.

        Arguments:
            (input) data -> Log entry.

        """

        self.data = data


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
             "dtg": False,
             "date": False,
             "stype": "encoded",
             "archive": False}]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_categorized_text2 -> Test with no categorized text.
        test_categorized_text -> Test with categorized text.
        test_confidence2 -> Test with confidence not equal to 1.
        test_confidence -> Test with confidence equal to 1.
        test_get_textract_data -> Test with extracting data.

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

        mock_extract.return_value = self.text
        mock_chardet.return_value = self.data
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text2

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            [])

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

        mock_extract.return_value = self.text
        mock_chardet.return_value = self.data
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            self.results)

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

        mock_extract.return_value = self.text
        mock_chardet.return_value = self.data2
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            self.results)

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

        mock_extract.return_value = self.text
        mock_chardet.return_value = self.data
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            self.results)

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

        mock_extract.return_value = self.text
        mock_chardet.return_value = self.data
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_sum.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_textract_data(self.f_name, self.cfg, self.logger),
            self.results)


if __name__ == "__main__":
    unittest.main()
