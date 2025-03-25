# Classification (U)

"""Program:  find_tokens.py

    Description:  Integration testing of find_tokens in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/find_tokens.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import PyPDF2
from nltk.tokenize import word_tokenize

# Local
sys.path.append(os.getcwd())
import rmq_metadata                             # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
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

        self.categorized_text = [
            ('First', 'O'), ('up', 'O'), ('in', 'O'),
            ('London', 'LOCATION'), ('will', 'O'), ('be', 'O'),
            ('Riccardo', 'PERSON'), ('Tisci', 'PERSON'), (',', 'O'),
            ('onetime', 'O'), ('Givenchy', 'ORGANIZATION'),
            ('darling', 'O'), (',', 'O'), ('favorite', 'O'),
            ('of', 'O'), ('Kardashian', 'PERSON'), ('-', 'O'),
            ('Jenners', 'O'), ('everywhere', 'O'), (',', 'O'),
            ('who', 'O'), ('returns', 'O'), ('to', 'O'), ('the', 'O'),
            ('catwalk', 'O'), ('with', 'O'), ('Burberry', 'O'),
            ('after', 'O'), ('the', 'O'), ('departure', 'O'),
            ('of', 'O'), ('Chri', 'O'), ('stopher', 'O'),
            ('Bailey', 'PERSON'), ('.', 'O')]

        # Read in PDF file.
        pdf_dir = os.path.join(base_path, "testfiles")
        self.filename = os.path.join(pdf_dir, "TestPDF.pdf")
        pdf = open(                                     # pylint:disable=R1732
            self.filename, mode="rb", encoding="UTF-8")
        pdfreader = PyPDF2.PdfFileReader(pdf)
        text = ""
        count = 0
        num_pages = pdfreader.numPages

        while count < num_pages:
            page = pdfreader.getPage(count)
            count += 1
            text += page.extractText()

        self.tokens = word_tokenize(text)

    def test_categorized_data(self):

        """Function:  test_categorized_data

        Description:  Test with categorized data returned.

        Arguments:

        """

        self.assertEqual(rmq_metadata.find_tokens(
            self.tokens, self.cfg), self.categorized_text)

    def tearDown(self):

        """Function:  tearDown

        Description:  Cleanup of test environment.

        Arguments:

        """

        del sys.modules["rabbitmq"]


if __name__ == "__main__":
    unittest.main()
