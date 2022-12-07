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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import rmq_metadata
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import version

__version__ = version.__version__


def monitor_queue(cfg, log):

    """Function Stub:  monitor_queue

    Description:  This is a function stub for rmq_metadata.monitor_queue

    Arguments:

    """

    status = True

    if cfg and log:
        status = True

    return status


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_status_false
        test_status_true
        test_func_call
        tearDown

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
        self.func_dict = {"-M": monitor_queue}
        cmdline = [
            "./rmq_metadata.py", "-c", "rabbitmq", "-d", self.config_dir, "-M"]
        opt_val_list = ["-c", "-d", "-y"]
        self.args = gen_class.ArgParser(
            cmdline, opt_val=opt_val_list, do_parse=True)

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
        self.args.args_array.pop("-M")

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
