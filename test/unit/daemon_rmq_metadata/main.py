#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in daemon_rmq_metadata.py.

    Usage:
        test/unit/daemon_rmq_metadata/main.py

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
import daemon_rmq_metadata
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_start_remove -> Test with daemon start option, but pid file exist.
        test_start_exists -> Test with daemon start option but already running.
        test_pid_not_running -> Test with pid file and process not running.
        test_pid_running -> Test with pid file and process running.
        test_start_daemon -> Test main function with daemon start option.
        test_stop_daemon -> Test main function with daemon stop option.
        test_restart_daemon -> Test main function with daemon restart option.
        test_invalid_daemon -> Test main function with invalid option.
        test_arg_require_false -> Test main function with arg_require false.
        test_arg_require_true -> Test main function with arg_require true.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = {"-a": "start", "-c": "rabbitmq"}

    @mock.patch("daemon_rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.is_active",
                mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.arg_parser")
    def test_start_remove(self, mock_arg):

        """Function:  test_start_remove

        Description:  Test with daemon start option, but pid file exist.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.is_active",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.arg_parser")
    def test_start_exists(self, mock_arg):

        """Function:  test_start_exists

        Description:  Test with daemon start option, but already running.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.is_active", mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.arg_parser")
    def test_pid_not_running(self, mock_arg):

        """Function:  test_pid_not_running

        Description:  Test with pid file and process not running.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.is_active", mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.arg_parser")
    def test_pid_running(self, mock_arg):

        """Function:  test_pid_running

        Description:  Test with pid file and process running.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.arg_parser")
    def test_start_daemon(self, mock_arg):

        """Function:  test_start_daemon

        Description:  Test main function with daemon start option.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.arg_parser")
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.stop")
    def test_stop_daemon(self, mock_daemon, mock_arg):

        """Function:  test_stop_daemon

        Description:  Test main function with daemon stop option.

        Arguments:

        """

        self.args["-a"] = "stop"
        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.arg_parser")
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.restart")
    def test_restart_daemon(self, mock_daemon, mock_arg):

        """Function:  test_restart_daemon

        Description:  Test main function with daemon restart option.

        Arguments:

        """

        self.args["-a"] = "restart"
        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.arg_parser")
    def test_invalid_daemon(self, mock_arg):

        """Function:  test_invalid_daemon

        Description:  Test main function with invalid option.

        Arguments:

        """

        self.args["-a"] = "nostart"
        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.arg_parser")
    def test_arg_require_false(self, mock_arg):

        """Function:  test_arg_require_false

        Description:  Test main function with arg_require false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.arg_parser")
    def test_arg_require_true(self, mock_arg):

        """Function:  test_arg_require_true

        Description:  Test main function with arg_require true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_arg.arg_require.return_value = True

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_metadata.main)


if __name__ == "__main__":
    unittest.main()
