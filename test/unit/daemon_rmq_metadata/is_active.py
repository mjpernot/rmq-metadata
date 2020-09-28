#!/usr/bin/python
# Classification (U)

"""Program:  is_active.py

    Description:  Unit testing of is_active in daemon_rmq_metadata.py.

    Usage:
        test/unit/daemon_rmq_metadata/is_active.py

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
import collections
import mock

# Local
sys.path.append(os.getcwd())
import daemon_rmq_metadata
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_ps_found -> Test with process and pid found.
        test_no_ps -> Test with process name found, not pid.
        test_no_proc_name -> Test with pid found, but not process name.
        test_ps_not_found -> Test with pid not found

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        psutil = collections.namedtuple("PSUtil", "pid name")
        self.procs = [psutil(12345, "proc_name1"), psutil(12346, "proc_name2"),
                      psutil(12347, "proc_name3"), psutil(12348, "proc_name4")]
        self.procs2 = [psutil(12345, "proc_name1"),
                       psutil(12346, "proc_name2"),
                       psutil(12348, "daemon_rmq_meta")]
        self.pfile = "./test/unit/daemon_rmq_metadata/basefiles/pidfile.txt"
        self.pfile2 = "./test/unit/daemon_rmq_metadata/basefiles/pidfile2.txt"
        self.pfile3 = "./test/unit/daemon_rmq_metadata/basefiles/pidfile3.txt"
        self.proc_name = "daemon_rmq_meta"

    @mock.patch("daemon_rmq_metadata.psutil.process_iter")
    def test_ps_found(self, mock_ps):

        """Function:  test_ps_found

        Description:  Test with process and pid found.

        Arguments:

        """

        mock_ps.return_value = self.procs2

        self.assertTrue(daemon_rmq_metadata.is_active(self.pfile3,
                                                      self.proc_name))

    @mock.patch("daemon_rmq_metadata.psutil.process_iter")
    def test_no_ps(self, mock_ps):

        """Function:  test_no_ps

        Description:  Test with process name found, not pid.

        Arguments:

        """

        mock_ps.return_value = self.procs2

        self.assertFalse(daemon_rmq_metadata.is_active(self.pfile2,
                                                       self.proc_name))

    @mock.patch("daemon_rmq_metadata.psutil.process_iter")
    def test_no_proc_name(self, mock_ps):

        """Function:  test_no_proc_name

        Description:  Test with pid found, but not process name.

        Arguments:

        """

        mock_ps.return_value = self.procs

        self.assertFalse(daemon_rmq_metadata.is_active(self.pfile2,
                                                       self.proc_name))

    @mock.patch("daemon_rmq_metadata.psutil.process_iter")
    def test_ps_not_found(self, mock_ps):

        """Function:  test_ps_not_found

        Description:  Test with pid not found.

        Arguments:

        """

        mock_ps.return_value = self.procs

        self.assertFalse(daemon_rmq_metadata.is_active(self.pfile,
                                                       self.proc_name))


if __name__ == "__main__":
    unittest.main()
