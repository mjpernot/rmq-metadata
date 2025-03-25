#!/usr/bin/python
# Classification (U)

"""Program:  publish_to_rmq.py

    Description:  Publish a PDF file to RabbitMQ in integration testing.

    Usage:
        test/integration/rmq_metadata/publish_to_rmq.py

    Arguments:
        filename

"""

# Libraries and Global Variables

# Standard
import os
import sys
import base64
import email.Parser

# Local
sys.path.append(os.getcwd())
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import rabbit_lib.rabbitmq_class as rcls    # pylint:disable=E0401,C0413,R0402


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


def main():

    """Function:  main

    Description:  Initializes program-wide variables and processes command
        line arguments and values.

    Arguments:

    """

    cmdline = gen_libs.get_inst(sys)
    fname = cmdline.argv[1]
    run_program(fname)


if __name__ == "__main__":
    sys.exit(main())
