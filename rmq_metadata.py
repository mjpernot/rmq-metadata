#!/usr/bin/python
# Classification (U)

"""Program:  rmq_metadata.py

    Description:  Processes PDFs from a RabbitMQ.  The program will offload a
        PDF file from a RabbitMQ, decode the PDF, extract meta-data from the
        PDF, tokenize and classify the meta-data.  The meta-data will then be
        summarized and inserted into a Mongo database and the PDF written to a
        file.

    Usage:
        rmq_metadata.py -c config_file -d dir_path {-M}
            [-v | -h]

    Arguments:
        -c config_file => RabbitMQ/Mongo configuration file.
            Required argument.
        -d dir_path => Directory path for option '-c'.
            Required argument.
        -M => Monitor and process messages from a RabbitMQ queue.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.

    Notes:
        The option to monitor the RabbitMQ is setup to run in an infinite loop
        and can only be killed with a CTRL-C on the command line, stopping the
        daemon, or shutting down of the service.

        RabbitMQ configuration file format (config/rabbitmq.py.TEMPLATE).

            # RabbitMQ Configuration file
            user = "USER"
            japd = "PASSWORD"
            host = "HOSTNAME"
            # RabbitMQ Exchange name being monitored.
            exchange_name = "EXCHANGE_NAME"
            # Email address(es) to send non-processed messages to or None.
            # None state no emails are required to be sent.
            to_line = "EMAIL_ADDRESS"|None
            # RabbitMQ listening port, default is 5672.
            port = 5672
            # Type of exchange:  direct, topic, fanout, headers
            exchange_type = "direct"
            # Is exchange durable: True|False
            x_durable = True
            # Are queues durable: True|False
            q_durable = True
            # Queues automatically delete message after processing: True|False
            auto_delete = False
            # Directory name for non-processed messages.
            message_dir = "DIRECTORY_PATH/message_dir"
            # Directory name for log files.
            log_dir = "DIRECTORY_PATH/logs"
            # File name to program log.
            log_file = "rmq_metadata.log"
            # Directory name for archived messages.
            # Must be set if archive in any of the queues is set to True.
            archive_dir = "DIRECTORY_PATH/archive"|None
            # Directory name for temporary message processing.
            tmp_dir = "DIRECTORY_PATH/tmp"
            # These entries for the Stanford NLP library module.
            # Path to Stanford language module.
            # By default lang_module will point to the English language module.
            lang_module =
            "DIRECTORY_PATH/classifiers/english.all.3class.distsim.crf.ser.gz"
            # Path to Stanford jar.
            stanford_jar = "DIRECTORY_PATH/stanford-ner.jar"
            # Encoding code for Stanford module.
            # Default setting is the utf-8 encoding code.
            encoding = "utf-8"
            # List of Token types.
            # Do not change unless you understand Stanford NLP and textract
            #   modules.
            token_types = ["LOCATION", "PERSON", "ORGANIZATION"]
            # List of textract module decodes.
            # Do not change unless you understand textract module.
            textract_codes = ["utf-8", "ascii", "iso-8859-1"]
            # List of queues to monitor.
            # Make a copy of the dictionary for each combination of a queue
                name and routing key.
            # -> queue:  "QUEUE_NAME" - Name of queue to monitor.
            # -> routing_key:  "ROUTING_KEY" - Name of routing key for queue.
            # -> directory:  "/DIR_PATH" - Directory path to where a PDF will
                be written to.
            # -> prename:  "NAME" - Static pre-file name string.
            # -> postname:  "NAME" - Static post-file name string.
            # -> mode:  "a"|"w" - Write mode to the file.
            # -> ext:  "pdf" - Extension name to the file name.
            # -> stype:  "encode" - Require the PDF file to be decoded.
            # -> archive:  True|False - Archive the RMQ body.
            queue_list = [
                    {"queue": "QUEUE_NAME",
                     "routing_key": "ROUTING_KEY",
                     "directory": "DIR_PATH",
                     "prename": "",
                     "postname": "",
                     "mode": "w",
                     "ext": "pdf",
                     "stype": "encoded",
                     "archive": True
                    },
                    {"queue": "QUEUE_NAME",
                     "routing_key": "ROUTING_KEY",
                     "directory": "DIR_PATH",
                     "prename": "",
                     "postname": "",
                     "mode": "w",
                     "ext": "pdf",
                     "dtg": False,
                     "date":  False,
                     "stype": "encoded",
                     "flatten": True
                    }
                ]
            # Mongo configuration file
            # Default is the name used in the README setup.
            mongo_cfg = "mongo"
            # Mongo config setup.
            # For internal use.  Do not change.
            mongo = None

        Mongo configuration file format (config/mongo.py.TEMPLATE).

            # Mongo DB Configuration file
            # All Mongo configuration settings.
            user = "USER"
            japd = "PSWORD"
            # Mongo DB host information
            host = "IP_ADDRESS"
            name = "HOSTNAME"
            # Mongo database port (default is 27017)
            port = 27017
            # Mongo configuration settings
            conf_file = None
            # Authentication required:  True|False
            auth = True
            # Name of Mongo database.
            db = "DATABASE"
            # Name of Mongo table/collection.
            tbl = "TABLE"
            # Replica Set Mongo configuration settings.
            # None means the Mongo database is not part of a replica set.
            # Replica set name.
            #    Format:  repset = "REPLICA_SET_NAME"
            repset = None
            # Replica host listing.
            #    Format:  repset_hosts = "HOST1:PORT, HOST2:PORT, [...]"
            repset_hosts = None
            # Database to authentication to.
            #    Format:  db_auth = "AUTHENTICATION_DATABASE"
            db_auth = None

    Example:
        Command Line:
            rmq_metadata.py -c rabbitmq -d config -M

        Daemon:
            daemon_rmq_metadata.py -a start -c rabbitmq -d /path/config -M

        Service:
            service rmq_metadata start

"""

# Libraries and Global Variables

# Standard
import sys
import os
import socket
import getpass
import datetime

# Third-party
import ast
import json
import base64
import chardet
import PyPDF2
import textract
from nltk.tokenize import word_tokenize
from nltk.tag import StanfordNERTagger

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
import mongo_lib.mongo_libs as mongo_libs
import version

__version__ = version.__version__

# Global
DTG_FORMAT = "%Y-%m-%d_%H:%M:%S"


def help_message(**kwargs):

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def validate_create_settings(cfg, **kwargs):

    """Function:  validate_create_settings

    Description:  Validate the configuration settings and creation of certain
        settings.

    Arguments:
        (input) cfg -> Configuration module name.
        (output) cfg -> Configuration module handler.
        (output) status_flag -> True|False - successfully validation/creation.
        (output) err_msg -> Error message from checks.

    """

    err_msg = ""
    status_flag = True
    base_dir = gen_libs.get_base_dir(__file__)

    if not os.path.isabs(cfg.message_dir):
        cfg.message_dir = os.path.join(base_dir, cfg.message_dir)

    status, msg = gen_libs.chk_crt_dir(cfg.message_dir, write=True, read=True,
                                       no_print=True)

    if not status:
        err_msg = err_msg + msg
        status_flag = False

    if not os.path.isabs(cfg.log_dir):
        cfg.log_dir = os.path.join(base_dir, cfg.log_dir)

    status, msg = gen_libs.chk_crt_dir(cfg.log_dir, write=True, read=True,
                                       no_print=True)

    if status:
        base_name, ext_name = os.path.splitext(cfg.log_file)
        log_name = base_name + "_" + cfg.exchange_name + ext_name
        cfg.log_file = os.path.join(cfg.log_dir, log_name)

    else:
        err_msg = err_msg + msg
        status_flag = False

    if cfg.archive_dir and not os.path.isabs(cfg.archive_dir):
        cfg.archive_dir = os.path.join(base_dir, cfg.archive_dir)

    if cfg.archive_dir:
        status, msg = gen_libs.chk_crt_dir(cfg.archive_dir, write=True,
                                           read=True, no_print=True)

        if not status:
            err_msg = err_msg + msg
            status_flag = False

    if not os.path.isabs(cfg.tmp_dir):
        cfg.message_dir = os.path.join(base_dir, cfg.tmp_dir)

    status, msg = gen_libs.chk_crt_dir(cfg.tmp_dir, write=True, read=True,
                                       no_print=True)

    if not status:
        err_msg = err_msg + msg
        status_flag = False

    for queue in cfg.queue_list:
        status, msg = gen_libs.chk_crt_dir(queue["directory"], write=True,
                                           read=True, no_print=True)

        if not status:
            err_msg = err_msg + msg
            status_flag = False

    return cfg, status_flag, err_msg


def non_proc_msg(rmq, log, cfg, data, subj, r_key, **kwargs):

    """Function:  non_proc_msg

    Description:  Process non-processed messages.

    Arguments:
        (input) rmq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) data -> Body of message that was not processed.
        (input) subj -> Email subject line.
        (input) r_key -> Routing key for message.

    """

    global DTG_FORMAT

    log.log_info(
        "non_proc_msg:  Processing failed message: Routing Key: %s" % (r_key))
    frm_line = getpass.getuser() + "@" + socket.gethostname()
    rdtg = datetime.datetime.now()
    msecs = str(rdtg.microsecond / 100)
    dtg = datetime.datetime.strftime(rdtg, DTG_FORMAT) + "." + msecs
    f_name = rmq.exchange + "_" + r_key + "_" + dtg + ".txt"
    f_path = os.path.join(cfg.message_dir, f_name)
    subj = "rmq_metadata: " + subj
    line1 = "RabbitMQ message was not processed due to: %s" % (subj)
    line2 = "Exchange: %s, Routing Key: %s" % (rmq.exchange, r_key)
    line3 = "The body of the message is encoded data."
    line4 = "Body of message saved to: %s" % (f_path)

    if cfg.to_line:
        log.log_info("Sending email to: %s..." % (cfg.to_line))
        email = gen_class.Mail(cfg.to_line, subj, frm_line)
        email.add_2_msg(line1)
        email.add_2_msg(line2)
        email.add_2_msg(line3)
        email.add_2_msg(line4)
        email.send_mail()

    else:
        log.log_warn("No email being sent as TO line is empty.")

    log.log_err(line1)
    log.log_err(line2)
    log.log_err(line3)
    log.log_err(line4)
    gen_libs.write_file(f_path, data=data, mode="w")


def process_msg(rmq, log, cfg, method, body, **kwargs):

    """Function:  process_msg

    Description:  Process message from RabbitMQ queue.

    Arguments:
        (input) rmq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) method -> Delivery properties.
        (input) body -> Message body.

    """

    global DTG_FORMAT

    r_key = method.routing_key
    queue = None
    log.log_info(
        "process_msg:  Processing message body from Routing Key: %s" % (r_key))

    for item in cfg.queue_list:

        if item["routing_key"] == r_key:
            queue = item

            if queue["archive"] and cfg.archive_dir:
                rdtg = datetime.datetime.now()
                msecs = str(rdtg.microsecond / 100)
                dtg = datetime.datetime.strftime(rdtg, DTG_FORMAT) + \
                    "." + msecs
                f_name = rmq.exchange + "_" + queue["routing_key"] + "_" + \
                    dtg + ".body"
                f_path = os.path.join(cfg.archive_dir, f_name)
                log.log_info(
                    "process_msg:  Archiving message to: %s" % (f_path))
                gen_libs.write_file(f_path, data=body, mode="w")

            break

    if queue:
        _convert_data(rmq, log, cfg, queue, body, r_key)

    else:
        non_proc_msg(rmq, log, cfg, body, "No queue detected", r_key)


def _convert_data(rmq, log, cfg, queue, body, r_key, **kwargs):

    """Function:  _convert_data

    Description:  Private function to process message queue.

    Arguments:
        (input) rmq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) queue -> RabbitMQ queue.
        (input) body -> Message body.
        (input) r_key -> Routing key.

    """

    prename = ""
    postname = ""
    ext = ""
    log.log_info("_convert_data:  Converting data in message body.")
    rdtg = datetime.datetime.now()
    msecs = str(rdtg.microsecond / 100)
    dtg = datetime.datetime.strftime(rdtg, "%Y%m%d%H%M%S") + "." + msecs
    t_filename = "tmp_" + rmq.exchange + "_" + r_key + "_" + dtg + ".txt"
    t_file = os.path.join(cfg.tmp_dir, t_filename)

    if queue["prename"]:
        prename = queue["prename"] + "_"

    if queue["postname"]:
        postname = "_" + queue["postname"]

    if queue["ext"]:
        ext = "." + queue["ext"]

    f_filename = prename + rmq.exchange + "_" + r_key + "_" + dtg + \
        postname + ext
    f_name = os.path.join(cfg.tmp_dir, f_filename)
    log.log_info("Starting processing of: %s" % (f_name))
    gen_libs.write_file(t_file, data=body, mode="w")

    if queue["stype"] == "encoded":
        log.log_info("_convert_data:  Decoding data in message body.")
        base64.decode(open(t_file, 'rb'), open(f_name, 'wb'))
        os.remove(t_file)

    else:
        log.log_info("_convert_data:  No encoding setting detected.")
        gen_libs.rename_file(t_filename, f_filename, cfg.tmp_dir)

    _process_queue(queue, body, r_key, cfg, f_name, log)


def read_pdf(filename, **kwargs):

    """Function:  read_pdf

    Description:  Extract text from a PDF file using the PyPDF2 module.

    Arguments:
        (input) filename -> PDF file name.

    """

    pdf = open(filename, "rb")
    pdfreader = PyPDF2.PdfFileReader(pdf)
    num_pages = pdfreader.numPages
    count = 0
    text = ""

    while count < num_pages:
        page = pdfreader.getPage(count)
        count += 1
        text += page.extractText()

    return text


def find_tokens(tokenized_text, cfg, **kwargs):

    """Function:  find_tokens

    Description:  Using the Stanford NLP module to classify a list of set of
        tokens.

    Arguments:
        (input) tokenized_text -> List of tokens.
        (input) cfg -> Configuration settings module for the program.
        (output) categorized_text -> List of categorized tokens.

    """

    tokenized_text = list(tokenized_text)
    snt = StanfordNERTagger(cfg.lang_module, cfg.stanford_jar, cfg.encoding)
    categorized_text = snt.tag(tokenized_text)

    return categorized_text


def summarize_data(categorized_text, token_types, **kwargs):

    """Function:  summarize_data

    Description:  Summarize a list of categorized tokens and merging them into
        a single unique list.

    Arguments:
        (input) categorized_text -> List of categorized tokens.
        (input) token_types -> List of token types to be accepted.
        (output) data_list -> List of summarized categorized tokens.

    """

    categorized_text = list(categorized_text)
    token_types = list(token_types)
    data_list = []
    tmp_data = []
    current_type = ""

    for item in categorized_text:
        current_type, data_list, tmp_data = _sort_data(
            item, current_type, data_list, tmp_data, token_types)

    else:
        if tmp_data:
            data_list = merge_data(data_list, tmp_data)

    return data_list


def _sort_data(item, current_type, data_list, tmp_data, token_types, **kwargs):

    """Function:  _sort_data

    Description:  Private function for summarize_data.  Combines a series of
        same token types into a data set and ignores the "O" (OTHER) token
        type.

    Arguments:
        (input) item -> Single set token.
        (input) current_type -> Current token type.
        (input) data_list -> List of summarized categorized tokens.
        (input) tmp_data -> List of current series of token data.
        (input) token_types -> List of token types.
        (output) current_type -> Current token type.
        (output) data_list -> List of summarized categorized tokens.
        (output) tmp_data -> List of current series of token data.

    """

    data_list = list(data_list)
    tmp_data = list(tmp_data)
    token_types = list(token_types)

    if item[1] == "O":
        current_type = item[1]

        if tmp_data:
            data_list = merge_data(data_list, tmp_data)
            tmp_data = []

    elif item[1] in token_types and item[1] == current_type:
        tmp_data.append(item)

    elif item[1] in token_types:
        if tmp_data:
            data_list = merge_data(data_list, tmp_data)

        tmp_data = []
        tmp_data.append(item)
        current_type = item[1]

    return current_type, data_list, tmp_data


def merge_data(data_list, tmp_data, **kwargs):

    """Function:  merge_data

    Description:  Adds a series of similar token data into a single string
        and adds the token type and string as set to a list.

    Arguments:
        (input) data_list -> List of summarized categorized tokens.
        (input) tmp_data -> List of current series of token data.
        (output) data_list -> List of summarized categorized tokens.

    """

    data_list = list(data_list)
    tmp_data = list(tmp_data)
    data = tmp_data.pop(0)
    tmp_a = data[0]
    data_type = data[1]

    for item in tmp_data:
        tmp_a = tmp_a + " " + item[0]

    data_list.append((tmp_a, data_type))

    return data_list


def get_pypdf2_data(f_name, cfg, log, **kwargs):

    """Function:  get_pypdf2_data

    Description:  Tokenize, categorize, summarize the raw data from the PDF
        file extracted using PyPDF2 module.

    Arguments:
        (input) f_name -> PDF file name.
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.
        (output) final_data -> List of categorized tokens from PDF file.

    """

    log.log_info("get_pypdf2_data:  Extracting data using PyPDF2.")
    final_data = []
    rawtext = read_pdf(f_name)
    log.log_info("get_pypdf2_data:  Running word_tokenizer...")
    tokens = word_tokenize(rawtext)
    log.log_info("get_pypdf2_data:  Finding tokens.")
    categorized_text = find_tokens(tokens, cfg)

    if categorized_text:
        log.log_info("get_pypdf2_data:  Summarizing data")
        final_data = summarize_data(categorized_text, cfg.token_types)

    return final_data


def create_metadata(metadata, data, **kwargs):

    """Function:  create_metadata2

    Description:  Merge a list of data sets into an existing dictionary based
        on the keys in the dictionary or create new keys in the dictionary
        based on the data set in the list.

    Arguments:
        (input) metadata -> Dictionary of meta-data.
        (input) data -> List of data sets.
        (output) metadata -> Dictionary of meta-data.

    """

    data = list(data)

    for item in data:

        # Create new key.
        if item[1] not in metadata.keys():
            metadata[item[1]] = [item[0]]

        # Check for duplicate entry in dictionary's list.
        elif item[0] not in metadata[item[1]]:
            metadata[item[1]].append(item[0])

    return metadata


def extract_pdf(f_name, char_encoding=None, **kwargs):

    """Function:  extract_pdf

    Description:  Extract text from PDF using textract module.

    Arguments:
        (input) f_name -> PDF file name.
        (input) char_encoding -> Character encoding code.
        (output) text -> Raw text.

    """

    if char_encoding:
        text = textract.process(f_name, encoding=char_encoding)

    else:
        text = textract.process(f_name)

    return text


def get_textract_data(f_name, cfg, log, **kwargs):

    """Function:  get_textract_data

    Description:  .

    Arguments:
        (input) f_name -> PDF file name.
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.
        (output) final_data -> List of categorized tokens from PDF file.

    """

    log.log_info("get_textract_data:  Extracting data using textract.")
    suberrstr = "codec can't decode byte"
    char_encoding = None
    status = True
    final_data = []

    # Get character encoding.
    log.log_info("get_textract_data:  Detecting encode in PDF file.")
    tmptext = extract_pdf(f_name)
    data = chardet.detect(tmptext)

    if data["confidence"] == 1.0:
        char_encoding = data["encoding"]
        log.log_info("get_textract_data:  Detected character encode: %s" %
                     (char_encoding))

    rawtext = extract_pdf(f_name, char_encoding)
    log.log_info("get_textract_data:  Running word_tokenizer...")

    try:
        tokens = word_tokenize(rawtext)

    except UnicodeDecodeError as msg:
        log.log_warn("get_textract_data:  UnicodeDecodeError detected.")

        if str(msg).find(suberrstr) >= 0 and msg.args[0] in cfg.textract_codes:
            char_encoding = msg.args[0]
            log.log_info("get_textract_data:  New encoding code detected: %s" %
                         (char_encoding))
            rawtext = extract_pdf(f_name, char_encoding)
            tokens = word_tokenize(rawtext)

        else:
            log.log_warn("get_textract_data:  No encoding code detected.")
            status = False

    if status:
        log.log_info("get_textract_data:  Finding tokens.")
        categorized_text = find_tokens(tokens, cfg)

        if categorized_text:
            log.log_info("get_textract_data:  Summarizing data")
            final_data = summarize_data(categorized_text, cfg.token_types)

    return final_data


def _process_queue(queue, body, r_key, cfg, f_name, log, **kwargs):

    """Function:  _process_queue

    Description:  Private function to process message queue.

    Arguments:
        (input) queue -> RabbitMQ queue.
        (input) body -> Message body.
        (input) r_key -> Routing key.
        (input) cfg -> Configuration settings module for the program.
        (input) f_name -> PDF file name.
        (input) log -> Log class instance.

    """

    global DTG_FORMAT

    log.log_info("_process_queue:  Extracting and processing metadata.")
    dtg = datetime.datetime.strftime(datetime.datetime.now(), DTG_FORMAT)
    filename = os.path.join(queue["directory"], os.path.basename(f_name))
    metadata = {"FileName": filename, "DateTime": dtg}

    # Use the PyPDF2 module to extract data.
    final_data = get_pypdf2_data(f_name, cfg, log)
    metadata = create_metadata(metadata, final_data)

    # Use the textract module to extract data.
    final_data = get_textract_data(f_name, cfg, log)
    metadata = create_metadata(metadata, final_data)

    log.log_info("_process_queue:  Insert metadata into MongoDB.")
    mongo_libs.ins_doc(cfg.mongo, cfg.mongo.dbs, cfg.mongo.tbl, metadata)
    log.log_info("_process_queue:  Moving PDF to: %s" % (queue["directory"]))
    gen_libs.mv_file2(f_name, os.path.dirname(filename),
                      os.path.basename(filename))
    log.log_info("Finished processing of: %s" % (f_name))


def monitor_queue(cfg, log, **kwargs):

    """Function:  monitor_queue

    Description:  Monitor RabbitMQ queue for messages.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.

    """

    def callback(channel, method, properties, body):

        """Function:  callback

        Description:  Process message from RabbitMQ.

        Arguments:
            (input) channel -> Channel properties.
            (input) method -> Delivery properties.
            (input) properties -> Properties of the message.
            (input) body -> Message body.

        """

        log.log_info("callback:  Processing message with Routing Key: %s" %
                     (method.routing_key))
        process_msg(rmq, log, cfg, method, body)
        log.log_info("Deleting message with Routing Key: %s" %
                     (method.routing_key))
        rmq.ack(method.delivery_tag)

    log.log_info("monitor_queue:  Initialize monitoring of queues...")

    for queue in cfg.queue_list:
        rmq = rabbitmq_class.RabbitMQCon(
            cfg.user, cfg.japd, cfg.host, cfg.port,
            exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
            queue_name=queue["queue"], routing_key=queue["routing_key"],
            x_durable=cfg.x_durable, q_durable=cfg.q_durable,
            auto_delete=cfg.auto_delete)

        log.log_info("Initializing:  Queue: %s, Routing Key: %s" %
                     (queue["queue"], queue["routing_key"]))
        connect_status, err_msg = rmq.create_connection()

        if connect_status and rmq.channel.is_open:
            log.log_info("Initialized RabbitMQ node: %s" % (queue["queue"]))

        else:
            log.log_err("Initialization failed RabbuitMQ: %s -> Msg: %s" %
                        (queue["queue"], err_msg))

        rmq.drop_connection()

    log.log_info("monitor_queue:  Start monitoring queue...")

    # Connect to first queue as only one connection required.
    rmq = rabbitmq_class.RabbitMQCon(
        cfg.user, cfg.japd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=cfg.queue_list[0]["queue"],
        routing_key=cfg.queue_list[0]["routing_key"],
        x_durable=cfg.x_durable, q_durable=cfg.q_durable,
        auto_delete=cfg.auto_delete)

    log.log_info("Connection info: %s->%s" % (cfg.host, cfg.exchange_name))
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        log.log_info("Connected to RabbitMQ node")

        # Setup the RabbitMQ Consume callback on multiple queues.
        for queue in cfg.queue_list:
            log.log_info("Monitoring RabbitMQ Queue: %s, Routing Key: %s" %
                         (queue["queue"], queue["routing_key"]))
            rmq.consume(callback, queue=queue["queue"])

        rmq.start_loop()

    else:
        log.log_err("Failed to connnect to RabbuitMQ -> Msg: %s" % (err_msg))


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Set a program lock to prevent other instantiations from running.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) func_dict -> Dict of function calls and associated options.

    """

    cmdline = gen_libs.get_inst(sys)
    args_array = dict(args_array)
    func_dict = dict(func_dict)
    cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])
    cfg.mongo = gen_libs.load_module(cfg.mongo_cfg, args_array["-d"])
    cfg, status_flag, err_msg = validate_create_settings(cfg)

    if status_flag:
        log = gen_class.Logger(cfg.log_file, cfg.log_file, "INFO",
                               "%(asctime)s %(levelname)s %(message)s",
                               "%Y-%m-%dT%H:%M:%SZ")
        str_val = "=" * 80
        log.log_info("%s:%s Initialized" % (cfg.host, cfg.exchange_name))
        log.log_info("%s" % (str_val))
        log.log_info("Exchange Name:  %s" % (cfg.exchange_name))
        log.log_info("Queue Configuration:")

        for queue in cfg.queue_list:
            log.log_info("\tQueue Name:  %s, Routing Key: %s" %
                         (queue["queue"], queue["routing_key"]))

        log.log_info("To Email:  %s" % (cfg.to_line))
        log.log_info("%s" % (str_val))

        try:
            flavor_id = cfg.exchange_name
            prog_lock = gen_class.ProgramLock(cmdline.argv, flavor_id)

            # Intersect args_array & func_dict to find which functions to call.
            for opt in set(args_array.keys()) & set(func_dict.keys()):
                func_dict[opt](cfg, log, **kwargs)

            del prog_lock

        except gen_class.SingleInstanceException:
            log.log_warn("rmq_metadata lock in place for: %s" % (flavor_id))

        log.log_close()

    else:
        print("Error:  Problem in configuration file or directory setup.")
        print(err_msg)


def main(**kwargs):

    """Function:  main

    Description:  Initializes program-wide variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        func_dict -> dictionary list for the function calls or other options.
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) sys.argv -> Arguments from the command line.
        (input) **kwargs:
            argv_list -> List of arguments from another program.

    """

    cmdline = gen_libs.get_inst(sys)
    cmdline.argv = list(kwargs.get("argv_list", cmdline.argv))
    dir_chk_list = ["-d"]
    func_dict = {"-M": monitor_queue}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):
        run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())
