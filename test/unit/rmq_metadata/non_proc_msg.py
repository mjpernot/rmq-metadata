#!/usr/bin/python
# Classification (U)

"""Program:  non_proc_msg.py

    Description:  Unit testing of non_proc_msg in rmq_metadata.py.

    Usage:
        test/unit/rmq_metadata/non_proc_msg.py

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
        test_to_empty_line -> Test for empty to line.
        test_to_line -> Test for valid to line.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.exchange = "test_exchange"
                self.to_line = ""
                self.message_dir = "message_dir"

        self.cfg = CfgTest()
        self.r_key = "Routing Key"
        self.data = "Line"
        self.subj = "Test_Subject"

    @mock.patch("rmq_metadata.gen_class.Mail")
    @mock.patch("rmq_metadata.gen_libs.write_file")
    @mock.patch("rmq_metadata.gen_class.Logger")
    def test_empty_to_line(self, mock_log, mock_write, mock_mail):

        """Function:  test_empty_to_line

        Description:  Test non_proc_msg function with empty to line.

        Arguments:

        """

        mock_log.return_value = True
        mock_write.return_value = True
        mock_mail.send_mail.return_value = True

        self.assertFalse(rmq_metadata.non_proc_msg(
            self.cfg, mock_log, self.cfg, self.data, self.subj, self.r_key))

    @mock.patch("rmq_metadata.gen_class.Mail")
    @mock.patch("rmq_metadata.gen_libs.write_file")
    @mock.patch("rmq_metadata.gen_class.Logger")
    def test_to_line(self, mock_log, mock_write, mock_mail):

        """Function:  test_to_line

        Description:  Test non_proc_msg function with valid to line.

        Arguments:

        """

        mock_log.return_value = True
        mock_write.return_value = True
        mock_mail.send_mail.return_value = True

        self.cfg.to_line = "Test_Email@email.domain"

        self.assertFalse(rmq_metadata.non_proc_msg(
            self.cfg, mock_log, self.cfg, self.data, self.subj, self.r_key))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        self.cfg = None


if __name__ == "__main__":
    unittest.main()
