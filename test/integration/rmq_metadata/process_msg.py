# Classification (U)

"""Program:  process_msg.py

    Description:  Integration testing of process_msg in rmq_metadata.py.

    Usage:
        test/integration/rmq_metadata/process_msg.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import base64
import email.Parser

# Local
sys.path.append(os.getcwd())
import rmq_metadata                             # pylint:disable=E0401,C0413
import lib.gen_class as gen_class           # pylint:disable=E0401,C0413,R0402
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import mongo_lib.mongo_class as mclass      # pylint:disable=E0401,C0413,R0402
import rabbit_lib.rabbitmq_class as rcls    # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


def parse_email_file(fname):

    """Function:  parse_email_file

    Description:  Open and parse an email from a file.

    Arguments:

    """

    parser = email.Parser.Parser()
    msg = parser.parse(open(                            # pylint:disable=R1732
        fname, mode="r", encoding="UTF-8"))

    return msg


def publish_msg(rmq, fname):

    """Function:  publish_msg

    Description:  Open an encoded PDF file and publish it to RabbitMQ.

    Arguments:

    """

    status = True
    err_msg = None

    with open(                                          # pylint:disable=R1732
            fname, mode="r", encoding="UTF-8") as f_hldr:
        body = f_hldr.read()

    if not rmq.publish_msg(body):
        err_msg = "\tError:  Failed to publish message to RabbitMQ."
        status = False

    return status, err_msg


def create_rq_pub(cfg):

    """Function:  create_rq_pub

    Description:  Create and return a RabbitMQ Publication instance.

    Arguments:

    """

    rmq = rcls.RabbitMQPub(
        cfg.user, cfg.japd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=cfg.queue_list[0]["queue"],
        routing_key=cfg.queue_list[0]["routing_key"],
        x_durable=cfg.x_durable, q_durable=cfg.q_durable,
        auto_delete=cfg.auto_delete)
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        return rmq

    print("Error:  Failed to connect to RabbitMQ as Publisher.")
    print(f"Error Message: {err_msg}")

    return None


def run_program(fname):

    """Function:  run_program

    Description:  Determine whether to process the file as a PDF file or as an
        email with a PDF attachment.  Then base64 encode the PDF to a file,
        load a configuration file, and then publish the PDF to a RabbitMQ
        queue.

    Arguments:

    """

    integration_dir = "test/integration/rmq_metadata"
    base_path = os.path.join(os.getcwd(), integration_dir)
    tmp_dir = os.path.join(base_path, "tmp")
    config_dir = os.path.join(base_path, "config")

    _, f_ext = os.path.splitext(fname)

    if f_ext == ".pdf":
        filename = fname

    # Assume an email for any other extension.
    else:
        msg = parse_email_file(fname)

        if msg.is_multipart():
            for item in msg.walk():
                if item.get_content_type() in ["application/pdf"]:
                    filename = os.path.join(tmp_dir, item.get_filename())
                    open(                               # pylint:disable=R1732
                        filename, mode="wb",
                        encoding="UTF-8").write(item.get_payload(decode=True))
                    break

    base64_file = filename + ".encoded"
    base64.encode(
        open(filename, mode="rb", encoding="UTF-8"),    # pylint:disable=R1732
        open(                                           # pylint:disable=R1732
            base64_file, mode="wb", encoding="UTF-8"))
    cfg = gen_libs.load_module("rabbitmq", config_dir)
    rmq = create_rq_pub(cfg)

    if rmq:
        status, err_msg = publish_msg(rmq, base64_file)

        if not status:
            print(f"Error Message:  {err_msg}")
            print("Error:  Publish failed\n")

    else:
        print("Error:  Failed to create RabbitMQ Publisher instance")

    os.remove(base64_file)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_metadata
        test_encrypted_pdf
        test_multiple_queue_archive
        test_multiple_queues
        test_archive_false
        test_archive_true
        test_queue_found
        test_queue_not_found
        test_no_queue_list
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
        self.cfg = gen_libs.load_module("rabbitmq", config_dir)
        self.cfg.mongo = gen_libs.load_module(self.cfg.mongo_cfg, config_dir)
        log_dir = os.path.join(base_path, "logs")
        self.pdf_dir = os.path.join(base_path, "testfiles")
        self.f_name1 = "TestPDF.pdf"
        self.f_name2 = "TestPDFe.pdf"
        self.f_name3 = "TestPDFa.pdf"
        self.filename1 = os.path.join(self.pdf_dir, self.f_name1)
        self.filename2 = os.path.join(self.pdf_dir, "TestPDFe.pdf")
        self.filename3 = os.path.join(self.pdf_dir, "TestPDFa.pdf")
        self.filename = ""
        self.log_file = os.path.join(log_dir, "rmq_metadata.log")
        self.msg_dir = os.path.join(base_path, "message_dir")
        self.archive = os.path.join(base_path, "archive")
        self.filter_name = self.cfg.exchange_name + "_" \
            + self.cfg.queue_list[0]["routing_key"] + "_*"
        self.logger = gen_class.Logger(
            self.log_file, self.log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")
        self.new_queue = {"queue": "rmq_metadata_test2",
                          "routing_key": "rmq_metadata_test2",
                          "directory": "/dir/path", "prename": "",
                          "postname": "", "mode": "w", "ext": "pdf",
                          "stype": "encoded", "archive": False}

        self.rmq = rcls.RabbitMQCon(
            self.cfg.user, self.cfg.japd, self.cfg.host, self.cfg.port,
            exchange_name=self.cfg.exchange_name,
            exchange_type=self.cfg.exchange_type,
            queue_name=self.cfg.queue_list[0]["queue"],
            routing_key=self.cfg.queue_list[0]["routing_key"],
            x_durable=self.cfg.x_durable, q_durable=self.cfg.q_durable,
            auto_delete=self.cfg.auto_delete)
        connect_status, err_msg = self.rmq.create_connection()

        if not connect_status or not self.rmq.channel.is_open:
            self.rmq.drop_connection()
            print("Error:  Unable to connect to RabbitMQ.")
            print(f"Message:  {err_msg}")
            self.skipTest("No connection to RabbitMQ.")

        self.mongo = mclass.Coll(
            self.cfg.mongo.name, self.cfg.mongo.user, self.cfg.mongo.japd,
            self.cfg.mongo.host, self.cfg.mongo.port, db=self.cfg.mongo.dbs,
            coll=self.cfg.mongo.tbl, auth=self.cfg.mongo.auth, use_arg=True,
            auth_db="admin")

        if not self.mongo.connect()[0]:
            print("Error:  Unable to connect to Mongo database.")
            self.skipTest("No connection to Mongo database.")

    def test_no_metadata(self):

        """Function:  test_no_metadata

        Description:  Test with no metadata detected.

        Arguments:

        """

        def callback(                                   # pylint:disable=W0613
                channel, method, properties, body):

            """Function:  callback

            Description:  Process message from RabbitMQ.

            Arguments:

            """

            rmq_metadata.process_msg(self.rmq, self.logger, self.cfg, method,
                                     body)
            self.rmq.ack(method.delivery_tag)

        run_program(self.filename1)
        data = {}
        self.rmq.consume(callback, queue=self.cfg.queue_list[0]["queue"])
        cnt = 0

        while self.rmq.channel._consumer_infos:         # pylint:disable=W0212
            if cnt == 0:
                self.rmq.channel.connection.process_data_events(time_limit=1)
                cnt += 1

            else:
                break

        self.rmq.drop_connection()

        if self.mongo.coll_cnt() == 1:
            data = self.mongo.coll_find1()
            self.filename = os.path.join(data["Directory"], data["FileName"])

        self.assertTrue("FileName" in list(data.keys()) and
                        "Directory" in list(data.keys()))

    def test_encrypted_pdf(self):

        """Function:  test_encrypted_pdf

        Description:  Test with encrypted PDF file.

        Arguments:

        """

        def callback(                                   # pylint:disable=W0613
                channel, method, properties, body):

            """Function:  callback

            Description:  Process message from RabbitMQ.

            Arguments:

            """

            rmq_metadata.process_msg(self.rmq, self.logger, self.cfg, method,
                                     body)
            self.rmq.ack(method.delivery_tag)

        run_program(self.filename2)
        self.rmq.consume(callback, queue=self.cfg.queue_list[0]["queue"])
        cnt = 0

        while self.rmq.channel._consumer_infos:         # pylint:disable=W0212
            if cnt == 0:
                self.rmq.channel.connection.process_data_events(time_limit=1)
                cnt += 1

            else:
                break

        self.rmq.drop_connection()

        f_list = gen_libs.list_filter_files(self.msg_dir, self.filter_name)

        self.assertTrue(f_list and len(f_list) == 1)

        self.filename = f_list[0]

    def test_multiple_queues_archive(self):

        """Function:  test_multiple_queue_archive

        Description:  Test with archiving message body with multiple queues.

        Arguments:

        """

        def callback(                                   # pylint:disable=W0613
                channel, method, properties, body):

            """Function:  callback

            Description:  Process message from RabbitMQ.

            Arguments:

            """

            rmq_metadata.process_msg(self.rmq, self.logger, self.cfg, method,
                                     body)
            self.rmq.ack(method.delivery_tag)

        self.cfg.queue_list.append(self.new_queue)
        run_program(self.filename1)
        data = {}
        self.rmq.consume(callback, queue=self.cfg.queue_list[0]["queue"])
        cnt = 0

        while self.rmq.channel._consumer_infos:         # pylint:disable=W0212
            if cnt == 0:
                self.rmq.channel.connection.process_data_events(time_limit=1)
                cnt += 1

            else:
                break

        self.rmq.drop_connection()

        if self.mongo.coll_cnt() == 1:
            data = self.mongo.coll_find1()
            self.filename = os.path.join(data["Directory"], data["FileName"])

        f_list = gen_libs.list_filter_files(self.archive, self.filter_name)

        self.assertTrue(f_list and len(f_list) == 1)

    def test_multiple_queues(self):

        """Function:  test_multiple_queues

        Description:  Test with multiple queues found in queue_list.

        Arguments:

        """

        def callback(                                   # pylint:disable=W0613
                channel, method, properties, body):

            """Function:  callback

            Description:  Process message from RabbitMQ.

            Arguments:

            """

            rmq_metadata.process_msg(self.rmq, self.logger, self.cfg, method,
                                     body)
            self.rmq.ack(method.delivery_tag)

        self.cfg.queue_list.append(self.new_queue)
        run_program(self.filename1)
        data = {}
        self.rmq.consume(callback, queue=self.cfg.queue_list[0]["queue"])
        cnt = 0

        while self.rmq.channel._consumer_infos:         # pylint:disable=W0212
            if cnt == 0:
                self.rmq.channel.connection.process_data_events(time_limit=1)
                cnt += 1

            else:
                break

        self.rmq.drop_connection()

        if self.mongo.coll_cnt() == 1:
            data = self.mongo.coll_find1()
            self.filename = os.path.join(data["Directory"], data["FileName"])

        self.assertTrue("FileName" in list(data.keys()) and
                        "Directory" in list(data.keys()))

    def test_archive_false(self):

        """Function:  test_archive_false

        Description:  Test with archiving turned off.

        Arguments:

        """

        def callback(                                   # pylint:disable=W0613
                channel, method, properties, body):

            """Function:  callback

            Description:  Process message from RabbitMQ.

            Arguments:

            """

            rmq_metadata.process_msg(self.rmq, self.logger, self.cfg, method,
                                     body)
            self.rmq.ack(method.delivery_tag)

        self.cfg.queue_list[0]["archive"] = False
        run_program(self.filename1)
        data = {}
        self.rmq.consume(callback, queue=self.cfg.queue_list[0]["queue"])
        cnt = 0

        while self.rmq.channel._consumer_infos:         # pylint:disable=W0212
            if cnt == 0:
                self.rmq.channel.connection.process_data_events(time_limit=1)
                cnt += 1

            else:
                break

        self.rmq.drop_connection()

        if self.mongo.coll_cnt() == 1:
            data = self.mongo.coll_find1()
            self.filename = os.path.join(data["Directory"], data["FileName"])

        f_list = gen_libs.list_filter_files(self.archive, self.filter_name)

        self.assertFalse(f_list)

    def test_archive_true(self):

        """Function:  test_archive_true

        Description:  Test with archiving turned on.

        Arguments:

        """

        def callback(                                   # pylint:disable=W0613
                channel, method, properties, body):

            """Function:  callback

            Description:  Process message from RabbitMQ.

            Arguments:

            """

            rmq_metadata.process_msg(self.rmq, self.logger, self.cfg, method,
                                     body)
            self.rmq.ack(method.delivery_tag)

        run_program(self.filename1)
        data = {}
        self.rmq.consume(callback, queue=self.cfg.queue_list[0]["queue"])
        cnt = 0

        while self.rmq.channel._consumer_infos:         # pylint:disable=W0212
            if cnt == 0:
                self.rmq.channel.connection.process_data_events(time_limit=1)
                cnt += 1

            else:
                break

        self.rmq.drop_connection()

        if self.mongo.coll_cnt() == 1:
            data = self.mongo.coll_find1()
            self.filename = os.path.join(data["Directory"], data["FileName"])

        f_list = gen_libs.list_filter_files(self.archive, self.filter_name)

        self.assertTrue(f_list and len(f_list) == 1)

    def test_queue_found(self):

        """Function:  test_queue_found

        Description:  Test with queue found in queue_list.

        Arguments:

        """

        def callback(                                   # pylint:disable=W0613
                channel, method, properties, body):

            """Function:  callback

            Description:  Process message from RabbitMQ.

            Arguments:

            """

            rmq_metadata.process_msg(self.rmq, self.logger, self.cfg, method,
                                     body)
            self.rmq.ack(method.delivery_tag)

        run_program(self.filename1)
        data = {}
        self.rmq.consume(callback, queue=self.cfg.queue_list[0]["queue"])
        cnt = 0

        while self.rmq.channel._consumer_infos:         # pylint:disable=W0212
            if cnt == 0:
                self.rmq.channel.connection.process_data_events(time_limit=1)
                cnt += 1

            else:
                break

        self.rmq.drop_connection()

        if self.mongo.coll_cnt() == 1:
            data = self.mongo.coll_find1()
            self.filename = os.path.join(data["Directory"], data["FileName"])

        self.assertTrue("FileName" in list(data.keys()) and
                        "Directory" in list(data.keys()))

    def test_queue_not_found(self):

        """Function:  test_queue_not_found

        Description:  Test with no queue found in queue_list.

        Arguments:

        """

        def callback(                                   # pylint:disable=W0613
                channel, method, properties, body):

            """Function:  callback

            Description:  Process message from RabbitMQ.

            Arguments:

            """

            self.cfg.queue_list[0]["routing_key"] = "NotMyKey"
            rmq_metadata.process_msg(self.rmq, self.logger, self.cfg, method,
                                     body)
            self.rmq.ack(method.delivery_tag)

        run_program(self.filename1)
        self.filename = ""
        self.rmq.consume(callback, queue=self.cfg.queue_list[0]["queue"])
        cnt = 0

        while self.rmq.channel._consumer_infos:         # pylint:disable=W0212
            if cnt == 0:
                self.rmq.channel.connection.process_data_events(time_limit=1)
                cnt += 1

            else:
                break

        self.rmq.drop_connection()

        f_list = gen_libs.list_filter_files(self.msg_dir, self.filter_name)

        self.assertTrue(f_list and len(f_list) == 1)

        if f_list and len(f_list) == 1:
            os.remove(f_list[0])

    def test_no_queue_list(self):

        """Function:  test_no_queue_list

        Description:  Test with an empty queue list.

        Arguments:

        """

        def callback(                                   # pylint:disable=W0613
                channel, method, properties, body):

            """Function:  callback

            Description:  Process message from RabbitMQ.

            Arguments:

            """

            self.cfg.queue_list = []
            rmq_metadata.process_msg(self.rmq, self.logger, self.cfg, method,
                                     body)
            self.rmq.ack(method.delivery_tag)

        run_program(self.filename1)
        self.filename = ""
        self.rmq.consume(callback, queue=self.cfg.queue_list[0]["queue"])
        cnt = 0

        while self.rmq.channel._consumer_infos:         # pylint:disable=W0212
            if cnt == 0:
                self.rmq.channel.connection.process_data_events(time_limit=1)
                cnt += 1

            else:
                break

        self.rmq.drop_connection()

        f_list = gen_libs.list_filter_files(self.msg_dir, self.filter_name)

        self.assertTrue(f_list and len(f_list) == 1)

        if f_list and len(f_list) == 1:
            os.remove(f_list[0])

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        self.mongo.coll.delete_many({})

        del sys.modules["rabbitmq"]
        del sys.modules["mongo"]

        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

        if os.path.isfile(self.filename):
            os.remove(self.filename)

        for item in gen_libs.list_filter_files(self.archive, self.filter_name):
            os.remove(item)


if __name__ == "__main__":
    unittest.main()
