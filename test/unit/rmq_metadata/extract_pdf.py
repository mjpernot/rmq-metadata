#!/usr/bin/python
# Classification (U)

"""Program:  extract_pdf.py

    Description:  Unit testing of extract_pdf in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/extract_pdf.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_encoding -> Test with extracting data with encoding.
        test_extract_pdf -> Test with extracting data.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.filename = "Filename.pdf"
        self.encoding = "ascii"
        self.text = "ASCII Text"
        self.text2 = "UTF-8 text"
        self.results = "ASCII Text"
        self.results2 = "UTF-8 text"

    @mock.patch("rmq_metadata.textract.process")
    def test_encoding(self, mock_tract):

        """Function:  test_encoding

        Description:  Test with extracting data with encoding.

        Arguments:

        """

        mock_tract.return_value = self.text

        self.assertEqual(rmq_metadata.extract_pdf(
            self.filename, char_encoding=self.encoding), self.results)

    @mock.patch("rmq_metadata.textract.process")
    def test_extract_pdf(self, mock_tract):

        """Function:  test_extract_pdf

        Description:  Test with extracting data.

        Arguments:

        """

        mock_tract.return_value = self.text2

        self.assertEqual(rmq_metadata.extract_pdf(self.filename),
                         self.results2)


if __name__ == "__main__":
    unittest.main()
