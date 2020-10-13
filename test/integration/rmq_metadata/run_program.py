#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Integration testing of run_program in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/run_program.py

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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def monitor_queue(cfg, log):

    """Function Stub:  monitor_queue

    Description:  This is a function stub for rmq_metadata.monitor_queue

    Arguments:
        cfg -> Stub argument holder.
        log -> Stub argument holder.

    """

    status = True

    if cfg and log:
        status = True

    return status


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_status_false -> Test with status is False.
        test_status_true -> Test with status is True.
        test_func_call -> Test with call to function.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        integration_dir = "test/integration/rmq_metadata"
        base_path = os.path.join(os.getcwd(), integration_dir)
        self.config_dir = os.path.join(base_path, "config")
        log_dir = os.path.join(base_path, "logs")
        self.cfg = gen_libs.load_module("rabbitmq", self.config_dir)
        b_name, ext = os.path.splitext(self.cfg.log_file)
        l_name = b_name + "_" + self.cfg.exchange_name + ext
        self.log_file = os.path.join(log_dir, l_name)
        self.args = {"-c": "rabbitmq", "-d": self.config_dir, "-M": True}
        self.func_dict = {"-M": monitor_queue}

    @mock.patch("rmq_metadata.gen_libs.load_module")
    def test_status_false(self, mock_load):

        """Function:  test_status_false

        Description:  Test run_program function with status is False.

        Arguments:

        """

        self.cfg.log_dir = "." + self.cfg.log_dir

        mock_load.return_value = self.cfg

        with gen_libs.no_std_out():
            rmq_metadata.run_program(self.args, self.func_dict)

        self.assertFalse(os.path.isfile(self.log_file))

    def test_status_true(self):

        """Function:  test_status_true

        Description:  Test run_program function with status is True.

        Arguments:

        """

        # Remove to skip "for" loop.
        self.args.pop("-M")

        rmq_metadata.run_program(self.args, self.func_dict)

        self.assertTrue(os.path.isfile(self.log_file))

        del sys.modules["mongo"]

    @mock.patch("rmq_metadata.monitor_queue")
    def test_func_call(self, mock_func):

        """Function:  test_func_call

        Description:  Test run_program function with call to function.

        Arguments:

        """

        mock_func.return_value = True

        rmq_metadata.run_program(self.args, self.func_dict)

        self.assertTrue(os.path.isfile(self.log_file))

        del sys.modules["mongo"]

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        del sys.modules["rabbitmq"]

        if os.path.isfile(self.log_file):
            os.remove(self.log_file)


if __name__ == "__main__":
    unittest.main()
