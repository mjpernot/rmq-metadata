#!/usr/bin/python
# Classification (U)

"""Program:  extract_pdf.py

    Description:  Integration testing of extract_pdf in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/extract_pdf.py

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
        test_encrypted2 -> Test with encrypted pdf file.
        test_encrypted -> Test with encrypted pdf file.
        test_encoding -> Test with extracting data with encoding.
        test_extract_pdf -> Test with extracting data.
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
        self.encoding = "ascii"
        line1 = "First up in London will be Riccardo Tisci, onetime "
        line2 = "Givenchy darling,\nfavorite of Kardashian-Jenners everywhere,"
        line3 = " who returns to the catwalk with\nmen\xe2\x80\x99s and "
        line4 = "women\xe2\x80\x99s wear after a year and a half away, this "
        line5 = "time to reimagine\nBurberry after the departure of "
        line6 = "Christopher Bailey.\n\n\x0c"
        self.text = line1 + line2 + line3 + line4 + line5 + line6
        line7 = "First up in London will be Riccardo Tisci, onetime Givenchy"
        line8 = " darling,\nfavorite of Kardashian-Jenners everywhere, who"
        line9 = " returns to the catwalk with\nmens and womens wear after a "
        line10 = "year and a half away, this time to reimagine\nBurberry after"
        line11 = " the departure of Christopher Bailey.\n\n\x0c"
        self.text2 = line7 + line8 + line9 + line10 + line11

    def test_encrypted2(self):

        """Function:  test_encrypted2

        Description:  Test with encrypted pdf file.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.extract_pdf(
                self.filename2, self.logger, char_encoding=self.encoding),
            (False, ""))

    def test_encrypted(self):

        """Function:  test_encrypted

        Description:  Test with encrypted pdf file.

        Arguments:

        """

        self.assertEqual(rmq_metadata.extract_pdf(self.filename2, self.logger),
                         (False, ""))

    def test_encoding(self):

        """Function:  test_encoding

        Description:  Test with extracting data with encoding.

        Arguments:

        """

        self.assertEqual(
            rmq_metadata.extract_pdf(
                self.filename1, self.logger, char_encoding=self.encoding),
            (True, self.text2))

    def test_extract_pdf(self):

        """Function:  test_extract_pdf

        Description:  Test with extracting data.

        Arguments:

        """

        self.assertEqual(rmq_metadata.extract_pdf(self.filename1, self.logger),
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
