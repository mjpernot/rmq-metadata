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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import daemon_rmq_metadata
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_require
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()
        self.opt_req = None
        self.opt_req2 = True

    def arg_require(self, opt_req):

        """Method:  arg_require

        Description:  Method stub holder for gen_class.ArgParser.arg_require.

        Arguments:

        """

        self.opt_req = opt_req

        return self.opt_req2

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_start_remove
        test_start_exists
        test_pid_not_running
        test_pid_running
        test_start_daemon
        test_stop_daemon
        test_restart_daemon
        test_invalid_daemon
        test_arg_require_false
        test_arg_require_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args3 = ArgParser()
        self.args4 = ArgParser()
        self.args.args_array = {"-a": "start", "-c": "rabbitmq"}
        self.args2.args_array = {"-a": "stop", "-c": "rabbitmq"}
        self.args3.args_array = {"-a": "restart", "-c": "rabbitmq"}
        self.args4.args_array = {"-a": "nostart", "-c": "rabbitmq"}

    @mock.patch("daemon_rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.is_active",
                mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    def test_start_remove(self, mock_arg):

        """Function:  test_start_remove

        Description:  Test with daemon start option, but pid file exist.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.is_active",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    def test_start_exists(self, mock_arg):

        """Function:  test_start_exists

        Description:  Test with daemon start option, but already running.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.os.remove", mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.is_active", mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    def test_pid_not_running(self, mock_arg):

        """Function:  test_pid_not_running

        Description:  Test with pid file and process not running.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.is_active", mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    def test_pid_running(self, mock_arg):

        """Function:  test_pid_running

        Description:  Test with pid file and process running.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    def test_start_daemon(self, mock_arg):

        """Function:  test_start_daemon

        Description:  Test main function with daemon start option.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.stop")
    def test_stop_daemon(self, mock_daemon, mock_arg):

        """Function:  test_stop_daemon

        Description:  Test main function with daemon stop option.

        Arguments:

        """

        mock_arg.return_value = self.args2
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.restart")
    def test_restart_daemon(self, mock_daemon, mock_arg):

        """Function:  test_restart_daemon

        Description:  Test main function with daemon restart option.

        Arguments:

        """

        mock_arg.return_value = self.args3
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    def test_invalid_daemon(self, mock_arg):

        """Function:  test_invalid_daemon

        Description:  Test main function with invalid option.

        Arguments:

        """

        mock_arg.return_value = self.args4
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.os.path.isfile",
                mock.Mock(return_value=False))
    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    def test_arg_require_false(self, mock_arg):

        """Function:  test_arg_require_false

        Description:  Test main function with arg_require false.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_arg.arg_require.return_value = False

        self.assertRaises(SystemExit, daemon_rmq_metadata.main)

    @mock.patch("daemon_rmq_metadata.RmqMetadataDaemon.start",
                mock.Mock(return_value=True))
    @mock.patch("daemon_rmq_metadata.gen_class.ArgParser")
    def test_arg_require_true(self, mock_arg):

        """Function:  test_arg_require_true

        Description:  Test main function with arg_require true.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_arg.arg_require.return_value = True

        #with gen_libs.no_std_out():
        self.assertRaises(SystemExit, daemon_rmq_metadata.main)


if __name__ == "__main__":
    unittest.main()
