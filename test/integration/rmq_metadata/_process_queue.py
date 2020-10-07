#!/usr/bin/python
# Classification (U)

"""Program:  _process_queue.py

    Description:  Integration testing of _process_queue in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/_process_queue.py

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
import lib.gen_libs as gen_libs
import mongo_lib.mongo_class as mongo_class
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_all_extract_fails -> Test with all extracts fails.
        test_all_successful_extracts -> Test with all successful extracts.
        tearDown -> Cleanup of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        integration_dir = "test/integration/rmq_metadata"
        base_path = os.path.join(os.getcwd(), integration_dir)
        config_dir = os.path.join(base_path, "config")
        self.final_dir = os.path.join(base_path, "final_data")
        self.tmp_dir = os.path.join(base_path, "tmp")
        self.cfg = gen_libs.load_module("rabbitmq", config_dir)
        self.cfg.mongo = gen_libs.load_module(self.cfg.mongo_cfg, config_dir)
        log_dir = os.path.join(base_path, "logs")
        self.pdf_dir = os.path.join(base_path, "testfiles")
        self.f_name1 = "TestPDF.pdf"
        self.f_name2 = "TestPDFe.pdf"
        self.f_name3 = "TestPDFa.pdf"
        self.filename1 = os.path.join(self.tmp_dir, "TestPDF.pdf")
        self.filename2 = os.path.join(self.tmp_dir, "TestPDFe.pdf")
        self.filename3 = os.path.join(self.tmp_dir, "TestPDFa.pdf")
        self.log_file = os.path.join(log_dir, "rmq_metadata.log")
        self.logger = gen_class.Logger(
            self.log_file, self.log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")

    def test_all_extract_fails(self):

        """Function:  test_all_extract_fails

        Description:  Test with all extracts fails.

        Arguments:

        """

        self.assertFalse(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.filename2, self.logger))

    def test_all_successful_extracts(self):

        """Function:  test_all_successful_extracts

        Description:  Test with all successful extracts.

        Arguments:

        """

        gen_libs.cp_file(self.f_name1, self.pdf_dir, self.tmp_dir)

        self.assertTrue(rmq_metadata._process_queue(
            self.cfg.queue_list[0], self.cfg, self.filename1, self.logger))

        mongo = mongo_class.Coll(
            self.cfg.mongo.name, self.cfg.mongo.user, self.cfg.mongo.japd,
            self.cfg.mongo.host, self.cfg.mongo.port, db=self.cfg.mongo.dbs,
            coll=self.cfg.mongo.tbl, auth=self.cfg.mongo.auth, use_arg=True,
            auth_db="admin")
        mongo.connect()
        if mongo.coll_cnt() == 1:
            data = mongo.coll_find1()

        STOPPED HERE - check data for correctness.

        mongo.coll.delete_many({})

    def tearDown(self):

        """Function:  tearDown

        Description:  Cleanup of test environment.

        Arguments:

        """

        del sys.modules["rabbitmq"]
        del sys.modules["mongo"]

        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

        if os.path.isfile(os.path.join(self.final_dir, self.f_name1)):
            os.remove(os.path.join(self.final_dir, self.f_name1))


if __name__ == "__main__":
    unittest.main()
