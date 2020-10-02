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

        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.f_name = "Filename.pdf"
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
            self.f_name, self.logger, char_encoding=self.encoding),
                         (True, self.results))

    @mock.patch("rmq_metadata.textract.process")
    def test_extract_pdf(self, mock_tract):

        """Function:  test_extract_pdf

        Description:  Test with extracting data.

        Arguments:

        """

        mock_tract.return_value = self.text2

        self.assertEqual(rmq_metadata.extract_pdf(self.f_name, self.logger),
                         (True, self.results2))


if __name__ == "__main__":
    unittest.main()
