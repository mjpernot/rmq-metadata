# Classification (U)

"""Program:  process_message.py

    Description:  Integration testing of process_message in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/process_message.py

    Arguments:

"""

# Libraries and Global Variables
from __future__ import print_function

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import rmq_metadata                             # pylint:disable=E0401,C0413
import lib.gen_class as gen_class           # pylint:disable=E0401,C0413,R0402
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import mongo_lib.mongo_class as mclass      # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_all_extract_fails
        test_all_successful_extracts2
        test_all_successful_extracts
        tearDown

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

        self.mongo = mclass.Coll(
            self.cfg.mongo.name, self.cfg.mongo.user, self.cfg.mongo.japd,
            self.cfg.mongo.host, self.cfg.mongo.port, db=self.cfg.mongo.dbs,
            coll=self.cfg.mongo.tbl, auth=self.cfg.mongo.auth, use_arg=True,
            auth_db="admin")

        if not self.mongo.connect()[0]:
            print("Error:  Unable to connect to Mongo database.")
            self.skipTest("No connection to Mongo database.")

    def test_no_data_extracted2(self):

        """Function:  test_no_data_extracted2

        Description:  Test with no data extracted.

        Arguments:

        """

        gen_libs.cp_file(self.f_name3, self.pdf_dir, self.tmp_dir)

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.filename3, self.logger))

    def test_no_data_extracted(self):

        """Function:  test_no_data_extracted

        Description:  Test with no data extracted.

        Arguments:

        """

        data = {}
        gen_libs.cp_file(self.f_name3, self.pdf_dir, self.tmp_dir)

        rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.filename3, self.logger)

        if self.mongo.coll_cnt() == 1:
            data = self.mongo.coll_find1()

        self.assertTrue(data["FileName"] == self.f_name3 and
                        data["Directory"] == self.final_dir and
                        ("LOCATION" not in list(data.keys()) and
                         "ORGANIZATION" not in list(data.keys()) and
                         "PERSON" not in list(data.keys())))

    def test_all_extract_fails(self):

        """Function:  test_all_extract_fails

        Description:  Test with all extracts fails.

        Arguments:

        """

        gen_libs.cp_file(self.f_name2, self.pdf_dir, self.tmp_dir)

        self.assertFalse(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.filename2, self.logger))

    def test_all_successful_extracts2(self):

        """Function:  test_all_successful_extracts2

        Description:  Test with all successful extracts.

        Arguments:

        """

        gen_libs.cp_file(self.f_name1, self.pdf_dir, self.tmp_dir)

        self.assertTrue(rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.filename1, self.logger))

    def test_all_successful_extracts(self):

        """Function:  test_all_successful_extracts

        Description:  Test with all successful extracts.

        Arguments:

        """

        data = {}
        gen_libs.cp_file(self.f_name1, self.pdf_dir, self.tmp_dir)

        rmq_metadata.process_message(
            self.cfg.queue_list[0], self.cfg, self.filename1, self.logger)

        if self.mongo.coll_cnt() == 1:
            data = self.mongo.coll_find1()

        self.assertTrue(data["FileName"] == self.f_name1 and
                        data["Directory"] == self.final_dir)

    def tearDown(self):

        """Function:  tearDown

        Description:  Cleanup of test environment.

        Arguments:

        """

        self.mongo.coll.delete_many({})

        del sys.modules["rabbitmq"]
        del sys.modules["mongo"]

        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

        if os.path.isfile(os.path.join(self.final_dir, self.f_name1)):
            os.remove(os.path.join(self.final_dir, self.f_name1))

        if os.path.isfile(os.path.join(self.tmp_dir, self.f_name2)):
            os.remove(os.path.join(self.tmp_dir, self.f_name2))

        if os.path.isfile(os.path.join(self.final_dir, self.f_name3)):
            os.remove(os.path.join(self.final_dir, self.f_name3))


if __name__ == "__main__":
    unittest.main()
