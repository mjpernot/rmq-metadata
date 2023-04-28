# Classification (U)

"""Program:  pdf_to_string.py

    Description:  Integration testing of pdf_to_string in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/pdf_to_string.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

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
        setUp
        test_encrypted
        test_pdf_to_string
        tearDown

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
        self.filename1 = os.path.join(pdf_dir, "TestPDFa.pdf")
        self.filename2 = os.path.join(pdf_dir, "TestPDFe.pdf")
        self.log_file = os.path.join(log_dir, "rmq_metadata.log")
        self.logger = gen_class.Logger(
            self.log_file, self.log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")

        self.text = \
            "This is a line of text to show no data is returned \n\n\x0c"

    def test_encrypted(self):

        """Function:  test_encrypted

        Description:  Test with multiple pages in document.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.pdf_to_string(self.filename2, self.logger),
            (False, ""))

    def test_pdf_to_string(self):

        """Function:  test_pdf_to_string

        Description:  Test with extracting data.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.pdf_to_string(self.filename1, self.logger),
            (True, self.text))

    def tearDown(self):

        """Function:  tearDown

        Description:  Cleanup of test environment.

        Arguments:

        """

        if os.path.isfile(self.log_file):
            os.remove(self.log_file)


if __name__ == "__main__":
    unittest.main()
