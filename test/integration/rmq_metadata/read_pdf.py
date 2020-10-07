#!/usr/bin/python
# Classification (U)

"""Program:  read_pdf.py

    Description:  Integration testing of read_pdf in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/read_pdf.py

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

# Local
sys.path.append(os.getcwd())
import rmq_metadata
import lib.gen_class as gen_class
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_is_encrypted -> Test with PDF encrypted.
        test_not_encrypted -> Test with PDF not encrypted.
        test_read_pdf -> Test with extracting data.
        tearDown -> Cleanup of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        integration_dir = "test/integration/rmq_metadata"
        base_path = os.path.join(os.getcwd(), integration_dir)
        log_dir = os.path.join(base_path, "logs")
        pdf_dir = os.path.join(base_path, "testfiles")
        self.filename1 = os.path.join(pdf_dir, "TestPDF.pdf")
        self.filename2 = os.path.join(pdf_dir, "TestPDFe.pdf")
        self.log_file = os.path.join(log_dir, "rmq_metadata.log")
        self.logger = gen_class.Logger(
            self.log_file, self.log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")

    def test_is_encrypted(self):

        """Function:  test_is_encrypted

        Description:  Test with PDF encrypted.

        Arguments:

        """

        status, text = rmq_metadata.read_pdf(self.filename2, self.logger)

        self.assertFalse(status)

    def test_not_encrypted(self):

        """Function:  test_not_encrypted

        Description:  Test with PDF not encrypted.

        Arguments:

        """

        status, text = rmq_metadata.read_pdf(self.filename1, self.logger)

        self.assertTrue(status)

    def test_read_pdf(self):

        """Function:  test_read_pdf

        Description:  Test with extracting data.

        Arguments:

        """

        status, text = rmq_metadata.read_pdf(self.filename1, self.logger)

        self.assertTrue(status)

    def tearDown(self):

        """Function:  tearDown

        Description:  Cleanup of test environment.

        Arguments:

        """

        if os.path.isfile(self.log_file):
            os.remove(self.log_file)


if __name__ == "__main__":
    unittest.main()
