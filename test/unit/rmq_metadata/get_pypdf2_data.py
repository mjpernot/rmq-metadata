# Classification (U)

"""Program:  get_pypdf2_data.py

    Description:  Unit testing of get_pypdf2_data in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/get_pypdf2_data.py

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

    def log_warn(self, data):

        """Method:  log_warn

        Description:  log_warn method.

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
        test_extract_failed
        test_extract_success
        test_no_categorized_data
        test_categorized_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.f_name = "FileName.pdf"
        self.cfg = CfgTest()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")

        if sys.version_info < (3, 0):
            self.rawtext = \
                u'Intheseunprecedentedtimeswewanttomakesurewecankeepin'
            self.tokens = [
                u'2.08', u'%', u'BalanceTransfer22.9', u'%', u'1.74']
            self.categorized_text = [
                (u',', u'O'), (u'London', u'LOCATION'), (u',', u'O'),
                (u'SW1W9AX', u'O')]
            self.final_data = {
                u'ORGANIZATION': [u'PAYPAL', u'HOMEBASE'],
                u'LOCATION': [u'London', u'Brighton', u'England', u'Wales'],
                u'PERSON': [u'John Street', u'SMITH'],
                'filename': 'mail2rmq_mail2rmq_file_20200924082706.1493.pdf',
                'datetime': '20200924_082717'}

        else:
            self.rawtext = \
                'Intheseunprecedentedtimeswewanttomakesurewecankeepin'
            self.tokens = [
                '2.08', '%', 'BalanceTransfer22.9', '%', '1.74']
            self.categorized_text = [
                (',', 'O'), ('London', 'LOCATION'), (',', 'O'),
                ('SW1W9AX', 'O')]
            self.final_data = {
                'ORGANIZATION': ['PAYPAL', 'HOMEBASE'],
                'LOCATION': ['London', 'Brighton', 'England', 'Wales'],
                'PERSON': ['John Street', 'SMITH'],
                'filename': 'mail2rmq_mail2rmq_file_20200924082706.1493.pdf',
                'datetime': '20200924_082717'}

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.read_pdf")
    def test_extract_failed(self, mock_read, mock_token, mock_find, mock_summ):

        """Function:  test_extract_failed

        Description:  Test with categorized data returned.

        Arguments:

        """

        mock_read.return_value = (False, "")
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_summ.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_pypdf2_data(self.f_name, self.cfg, self.logger),
            (False, []))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.read_pdf")
    def test_extract_success(self, mock_read, mock_token, mock_find,
                             mock_summ):

        """Function:  test_extract_success

        Description:  Test with extraction successful.

        Arguments:

        """

        mock_read.return_value = (True, self.rawtext)
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_summ.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_pypdf2_data(self.f_name, self.cfg, self.logger),
            (True, self.final_data))

    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.read_pdf")
    def test_no_categorized_data(self, mock_read, mock_token, mock_find):

        """Function:  test_no_categorized_data

        Description:  Test with no categorized data returned.

        Arguments:

        """

        mock_read.return_value = (True, self.rawtext)
        mock_token.return_value = self.tokens
        mock_find.return_value = []

        self.assertEqual(
            rmq_metadata.get_pypdf2_data(self.f_name, self.cfg, self.logger),
            (True, []))

    @mock.patch("rmq_metadata.summarize_data")
    @mock.patch("rmq_metadata.find_tokens")
    @mock.patch("rmq_metadata.word_tokenize")
    @mock.patch("rmq_metadata.read_pdf")
    def test_categorized_data(self, mock_read, mock_token, mock_find,
                              mock_summ):

        """Function:  test_categorized_data

        Description:  Test with categorized data returned.

        Arguments:

        """

        mock_read.return_value = (True, self.rawtext)
        mock_token.return_value = self.tokens
        mock_find.return_value = self.categorized_text
        mock_summ.return_value = self.final_data

        self.assertEqual(
            rmq_metadata.get_pypdf2_data(self.f_name, self.cfg, self.logger),
            (True, self.final_data))


if __name__ == "__main__":
    unittest.main()
