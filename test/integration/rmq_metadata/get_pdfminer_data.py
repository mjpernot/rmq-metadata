# Classification (U)

"""Program:  get_pdfminer_data.py

    Description:  Integration testing of get_pdfminer_data in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/get_pdfminer_data.py

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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_extract_failure
        test_no_categorized_text
        test_get_pdfminer_data
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        integration_dir = "test/integration/rmq_metadata"
        base_path = os.path.join(os.getcwd(), integration_dir)
        config_dir = os.path.join(base_path, "config")
        self.cfg = gen_libs.load_module("rabbitmq", config_dir)
        log_dir = os.path.join(base_path, "logs")
        pdf_dir = os.path.join(base_path, "testfiles")
        self.filename1 = os.path.join(pdf_dir, "TestPDF.pdf")
        self.filename2 = os.path.join(pdf_dir, "TestPDFe.pdf")
        self.filename3 = os.path.join(pdf_dir, "TestPDFa.pdf")
        self.log_file = os.path.join(log_dir, "rmq_metadata.log")
        self.logger = gen_class.Logger(
            self.log_file, self.log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")

        self.final_data = [
            (u'London', u'LOCATION'), (u'Riccardo Tisci', u'PERSON'),
            (u'Givenchy', u'ORGANIZATION'), (u'Christopher Bailey', u'PERSON')]

    def test_extract_failure(self):

        """Function:  test_extract_failure

        Description:  Test with failure of extraction.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.get_pdfminer_data(
                self.filename2, self.cfg, self.logger),
            (False, []))

    def test_no_categorized_text(self):

        """Function:  test_no_categorized_text

        Description:  Test with no categorized text.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.get_pdfminer_data(
                self.filename3, self.cfg, self.logger),
            (True, []))

    def test_get_pdfminer_data(self):

        """Function:  test_get_pdfminer_data

        Description:  Test with extracting data.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.get_pdfminer_data(
                self.filename1, self.cfg, self.logger),
            (True, self.final_data))

    def tearDown(self):

        """Function:  tearDown

        Description:  Cleanup of test environment.

        Arguments:

        """

        del sys.modules["rabbitmq"]

        if os.path.isfile(self.log_file):
            os.remove(self.log_file)


if __name__ == "__main__":
    unittest.main()
