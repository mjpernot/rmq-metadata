#!/usr/bin/python
# Classification (U)

"""Program:  pdf_to_string.py

    Description:  Unit testing of pdf_to_string in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/pdf_to_string.py

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


class BytesIO(object):

    """Class:  BytesIO

    Description:  Class which is a representation of a io class.

    Methods:
        __init__
        getvalue

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.data = "This is a test data string."

    def getvalue(self):

        """Method:  getvalue

        Description:  getvalue method.

        Arguments:

        """

        return self.data


class PDFPageInterpreter(object):

    """Class:  PDFPageInterpreter

    Description:  Class which is a representation of PDFPageInterpreter class.

    Methods:
        __init__
        process_page

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.page = None

    def process_page(self, page):

        """Method:  process_page

        Description:  process_page method.

        Arguments:

        """

        self.page = page


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_multiple_pages
        test_pdf_to_string

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.bytesio = BytesIO()
        self.interpreter = PDFPageInterpreter()
        self.tmpdir = "./test/unit/rmq_metadata/testfiles"
        self.f_name = os.path.join(self.tmpdir, "t_file.txt")
        self.page_list = ["Page1"]
        self.page_list2 = ["Page1", "Page2"]
        self.results = "This is a test data string"

    @mock.patch("rmq_metadata.TextConverter", mock.Mock(return_value="device"))
    @mock.patch("rmq_metadata.PDFResourceManager",
                mock.Mock(return_value="rsrcmgr"))
    @mock.patch("rmq_metadata.PDFDocument", mock.Mock(return_value="doc"))
    @mock.patch("rmq_metadata.PDFParser", mock.Mock(return_value="parser"))
    @mock.patch("rmq_metadata.PDFPage.create_pages")
    @mock.patch("rmq_metadata.PDFPageInterpreter")
    @mock.patch("rmq_metadata.BytesIO")
    def test_multiple_pages(self, mock_io, mock_inter, mock_pages):

        """Function:  test_multiple_pages

        Description:  Test with multiple pages in document.

        Arguments:

        """

        mock_io.return_value = self.bytesio
        mock_inter.return_value = self.interpreter
        mock_pages.return_value = self.page_list2

        self.assertEqual(
            rmq_metadata.pdf_to_string(self.f_name, self.logger),
            (True, self.results))

    @mock.patch("rmq_metadata.TextConverter", mock.Mock(return_value="device"))
    @mock.patch("rmq_metadata.PDFResourceManager",
                mock.Mock(return_value="rsrcmgr"))
    @mock.patch("rmq_metadata.PDFDocument", mock.Mock(return_value="doc"))
    @mock.patch("rmq_metadata.PDFParser", mock.Mock(return_value="parser"))
    @mock.patch("rmq_metadata.PDFPage.create_pages")
    @mock.patch("rmq_metadata.PDFPageInterpreter")
    @mock.patch("rmq_metadata.BytesIO")
    def test_pdf_to_string(self, mock_io, mock_inter, mock_pages):

        """Function:  test_pdf_to_string

        Description:  Test with extracting data.

        Arguments:

        """

        mock_io.return_value = self.bytesio
        mock_inter.return_value = self.interpreter
        mock_pages.return_value = self.page_list

        self.assertEqual(
            rmq_metadata.pdf_to_string(self.f_name, self.logger),
            (True, self.results))


if __name__ == "__main__":
    unittest.main()
