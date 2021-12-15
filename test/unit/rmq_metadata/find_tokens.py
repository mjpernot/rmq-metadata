#!/usr/bin/python
# Classification (U)

"""Program:  find_tokens.py

    Description:  Unit testing of find_tokens in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/find_tokens.py

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


class StanfordNERTagger(object):

    """Class:  StanfordNERTagger

    Description:  Class which is a representation of StanfordNERTagger class.

    Methods:
        __init__
        tag

    """

    def __init__(self, lang_module, stanford_jar, encoding):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.lang_module = lang_module
        self.stanford_jar = stanford_jar
        self.encoding = encoding
        self.tokenized_text = None
        self.categorized_text = [(u',', u'O'), (u'London', u'LOCATION'),
                                 (u',', u'O'), (u'SW1W9AX', u'O')]

    def tag(self, tokenized_text):

        """Method:  tag

        Description:  tag method.

        Arguments:

        """

        self.tokenized_text = tokenized_text

        return self.categorized_text


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
        test_categorized_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.tokenized_text = [u'2.08', u'%', u'BalanceTransfer22.9', u'%',
                               u'1.74']
        self.categorized_text = [(u',', u'O'), (u'London', u'LOCATION'),
                                 (u',', u'O'), (u'SW1W9AX', u'O')]
        self.cfg = CfgTest()
        self.nlp = StanfordNERTagger(self.cfg.lang_module,
                                     self.cfg.stanford_jar, self.cfg.encoding)

    @mock.patch("rmq_metadata.StanfordNERTagger")
    def test_categorized_data(self, mock_nlp):

        """Function:  test_categorized_data

        Description:  Test with categorized data returned.

        Arguments:

        """

        mock_nlp.return_value = self.nlp

        self.assertEqual(rmq_metadata.find_tokens(
            self.tokenized_text, self.cfg), self.categorized_text)


if __name__ == "__main__":
    unittest.main()
