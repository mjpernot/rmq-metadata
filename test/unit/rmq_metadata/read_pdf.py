#!/usr/bin/python
# Classification (U)

"""Program:  read_pdf.py

    Description:  Unit testing of read_pdf in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/read_pdf.py

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


class PageExtract(object):

    """Class:  PageExtract

    Description:  Class which is a representation of PageExtract class.

    Methods:
        __init__ -> Initialize configuration environment.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.body = u'Intheseunprecedentedtimeswewanttomakesurewecankeep'

    def extractText(self):

        """Method:  extractText

        Description:  Extract data from page.

        Arguments:

        """

        return self.body


class PyPDF2(object):

    """Class:  PyPDF2

    Description:  Class which is a representation of PyPDF2 class.

    Methods:
        __init__ -> Initialize configuration environment.
        getPage -> Data from page number passed.

    """

    def __init__(self, fname):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.fname = fname
        self.numPages = 1
        self.pagenum = None
        self.isEncrypted = False

    def getPage(self, pagenum):

        """Method:  getPage

        Description:  Data from page number passed.

        Arguments:
            (input) pagenum -> Page number of document.
            (output) Class instance of PageExtract.

        """

        self.pagenum = pagenum

        return PageExtract()


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_is_encrypted -> Test with PDF encrypted.
        test_not_encrypted -> Test with PDF not encrypted.
        test_read_pdf -> Test with extracting data.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.tmpdir = "./test/unit/rmq_metadata/testfiles"
        self.filename = os.path.join(self.tmpdir, "t_file.txt")
        self.pdfr = PyPDF2(self.filename)
        self.body = "Intheseunprecedentedtimeswewanttomakesurewecankeep"

    @mock.patch("rmq_metadata.PyPDF2.PdfFileReader")
    def test_is_encrypted(self, mock_pypdf):

        """Function:  test_is_encrypted

        Description:  Test with PDF encrypted.

        Arguments:

        """

        self.pdfr.isEncrypted = True

        mock_pypdf.return_value = self.pdfr

        self.assertEqual(rmq_metadata.read_pdf(self.filename, self.logger),
                         (False, ""))

    @mock.patch("rmq_metadata.PyPDF2.PdfFileReader")
    def test_not_encrypted(self, mock_pypdf):

        """Function:  test_not_encrypted

        Description:  Test with PDF not encrypted.

        Arguments:

        """

        mock_pypdf.return_value = self.pdfr

        self.assertEqual(rmq_metadata.read_pdf(self.filename, self.logger),
                         (True, self.body))

    @mock.patch("rmq_metadata.PyPDF2.PdfFileReader")
    def test_read_pdf(self, mock_pypdf):

        """Function:  test_read_pdf

        Description:  Test with extracting data.

        Arguments:

        """

        mock_pypdf.return_value = self.pdfr

        self.assertEqual(rmq_metadata.read_pdf(self.filename, self.logger),
                         (True, self.body))


if __name__ == "__main__":
    unittest.main()
