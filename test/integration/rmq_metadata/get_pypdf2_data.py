# Classification (U)

"""Program:  get_pypdf2_data.py

    Description:  Integration testing of get_pypdf2_data in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/get_pypdf2_data.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import rmq_metadata                             # pylint:disable=E0401,C0413
import lib.gen_class as gen_class           # pylint:disable=E0401,C0413,R0402
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_extract_failed
        test_extract_success
        test_no_categorized_data
        test_categorized_data
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
            ('London', 'LOCATION'), ('Riccardo Tisci', 'PERSON'),
            ('Givenchy', 'ORGANIZATION'), ('Kardashian', 'PERSON'),
            ('Bailey', 'PERSON')]

    def test_extract_failed(self):

        """Function:  test_extract_failed

        Description:  Test with categorized data returned.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.get_pypdf2_data(
                self.filename2, self.cfg, self.logger),
            (False, []))

    def test_extract_success(self):

        """Function:  test_extract_success

        Description:  Test with extraction successful.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.get_pypdf2_data(
                self.filename1, self.cfg, self.logger),
            (True, self.final_data))

    def test_no_categorized_data(self):

        """Function:  test_no_categorized_data

        Description:  Test with no categorized data returned.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.get_pypdf2_data(
                self.filename3, self.cfg, self.logger),
            (True, []))

    def test_categorized_data(self):

        """Function:  test_categorized_data

        Description:  Test with categorized data returned.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.get_pypdf2_data(
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
