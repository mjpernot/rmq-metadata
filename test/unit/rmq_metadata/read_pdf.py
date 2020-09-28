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


class PageExtract(object):

    """Class:  PageExtract

    Description:  Class which is a representation of PageExtract class.

    Methods:
        __init__ -> Initialize configuration environment.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the IsseGuard class.

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

        Description:  Initialization instance of the IsseGuard class.

        Arguments:

        """

        self.fname = fname
        self.numPages = 1
        self.pagenum = None

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
        test_read_pdf -> Test with extracting data.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.tmpdir = "./test/unit/rmq_metadata/testfiles"
        self.filename = os.path.join(self.tmpdir, "t_file.txt")
        self.pdfr = PyPDF2(self.filename)
        self.body = "Intheseunprecedentedtimeswewanttomakesurewecankeep"

    @mock.patch("rmq_metadata.PyPDF2.PdfFileReader")
    def test_read_pdf(self, mock_pypdf):

        """Function:  test_read_pdf

        Description:  Test with extracting data.

        Arguments:

        """

        mock_pypdf.return_value = self.pdfr

        self.assertEqual(rmq_metadata.read_pdf(self.filename), self.body)


if __name__ == "__main__":
    unittest.main()
