#!/usr/bin/python
# Classification (U)

"""Program:  rmq_metadata.py

    Description:  Processes PDFs from a RabbitMQ.  The program will offload a
        PDF file from a RabbitMQ, decode the PDF, extract meta-data from the
        PDF, tokenize and classify the meta-data.  The meta-data will then be
        summarized and saved to a metadata file and the PDF written to a file.

    Usage:
        rmq_metadata.py -c config_file -d dir_path {-M} [-y flavor_id]
            [-v | -h]

    Arguments:
        -c config_file => RabbitMQ configuration file.
        -d dir_path => Directory path for option '-c'.

        -M => Monitor and process messages from a RabbitMQ queue.

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.

    Notes:
        The option to monitor the RabbitMQ is setup to run in an infinite loop
        and can only be killed with a CTRL-C on the command line, stopping the
        daemon, or shutting down of the service.

        RabbitMQ configuration file format (config/rabbitmq.py.TEMPLATE).

            user = "USER"
            japd = "PSWORD"
            host = "HOSTNAME"
            exchange_name = "EXCHANGE_NAME"
            to_line = "EMAIL_ADDRESS@EMAIL_DOMAIN"
            port = 5672
            exchange_type = "direct"
            x_durable = True
            q_durable = True
            auto_delete = False
            base_dir = "DIRECTORY_PATH"
            message_dir = "message_dir"
            log_dir = "logs"
            log_file = "rmq_metadata.log"
            archive_dir = None
            tmp_dir = "tmp"
            lang_module =
            "DIRECTORY_PATH/classifiers/english.all.3class.distsim.crf.ser.gz"
            stanford_jar = "DIRECTORY_PATH/stanford-ner.jar"
            encoding = "utf-8"
            token_types = ["LOCATION", "PERSON", "ORGANIZATION"]
            textract_codes = ["utf-8", "ascii", "iso-8859-1"]
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
                }]

        Configuration modules -> Name is runtime dependent as it can be used to
            connect to different databases with different names.

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
import io
import base64
import chardet
import pypdf
import textract
from nltk.tokenize import word_tokenize
from nltk.tag import StanfordNERTagger
import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .rabbit_lib import rabbitmq_class
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs                     # pylint:disable=R0402
    import lib.gen_class as gen_class                   # pylint:disable=R0402
    import rabbit_lib.rabbitmq_class as rabbitmq_class  # pylint:disable=R0402
    import version

__version__ = version.__version__

# Global Variables


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def validate_create_settings(cfg):

    """Function:  validate_create_settings

    Description:  Validate the configuration settings and creation of certain
        settings.

    Arguments:
        (input) cfg -> Configuration module name
        (output) cfg -> Configuration module handler
        (output) status_flag -> True|False - successfully validation/creation
        (output) err_msg -> Error message from checks

    """

    err_msg = ""
    status_flag = True

    # Check on non-processed messages directory
    if not os.path.isabs(cfg.message_dir):
        cfg.message_dir = os.path.join(cfg.base_dir, cfg.message_dir)

    status, msg = gen_libs.chk_crt_dir(
        cfg.message_dir, write=True, read=True, no_print=True)

    if not status:
        err_msg = err_msg + msg
        status_flag = False

    # Check on log files directory.
    if not os.path.isabs(cfg.log_dir):
        cfg.log_dir = os.path.join(cfg.base_dir, cfg.log_dir)

    status, msg = gen_libs.chk_crt_dir(
        cfg.log_dir, write=True, read=True, no_print=True)

    if status:
        base_name, ext_name = os.path.splitext(cfg.log_file)
        log_name = base_name + "_" + cfg.exchange_name + ext_name
        cfg.log_file = os.path.join(cfg.log_dir, log_name)

    else:
        err_msg = err_msg + msg
        status_flag = False

    # Check on archived messages directory
    if cfg.archive_dir and not os.path.isabs(cfg.archive_dir):
        cfg.archive_dir = os.path.join(cfg.base_dir, cfg.archive_dir)

    if cfg.archive_dir:
        status, msg = gen_libs.chk_crt_dir(
            cfg.archive_dir, write=True, read=True, no_print=True)

        if not status:
            err_msg = err_msg + msg
            status_flag = False

    # Check on temporary message processing directory
    if not os.path.isabs(cfg.tmp_dir):
        cfg.tmp_dir = os.path.join(cfg.base_dir, cfg.tmp_dir)

    status, msg = gen_libs.chk_crt_dir(
        cfg.tmp_dir, write=True, read=True, no_print=True)

    if not status:
        err_msg = err_msg + msg
        status_flag = False

    # Check on file entries.
    status_flag, err_msg = validate_files(cfg, status_flag, err_msg)

    # Check on final directory for each queue
    for queue in cfg.queue_list:
        status, msg = gen_libs.chk_crt_dir(
            queue["directory"], write=True, read=True, no_print=True)

        if not status:
            err_msg = err_msg + msg
            status_flag = False

    return cfg, status_flag, err_msg


def validate_files(cfg, status_flag, err_msg):

    """Function:  validate_files

    Description:  Validates the file entries in the configuration file.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) status_flag -> True|False - successfully validation
        (input) err_msg -> Error message from checks
        (output) status_flag -> True|False - successfully validation
        (output) err_msg -> Error message from checks

    """

    # Check on Stanford NLP language module file
    if not os.path.isabs(cfg.lang_module):
        msg = f"lang_module not set to absolute path: {cfg.lang_module}"
        err_msg = err_msg + msg
        status_flag = False

    else:
        status, msg = gen_libs.chk_crt_file(
            cfg.lang_module, read=True, no_print=True)

        if not status:
            err_msg = err_msg + msg
            status_flag = False

    # Check on Stanford NLP jar file
    if not os.path.isabs(cfg.stanford_jar):
        msg = f"stanford_jar not set to absolute path: {cfg.stanford_jar}"
        err_msg = err_msg + msg
        status_flag = False

    else:
        status, msg = gen_libs.chk_crt_file(
            cfg.stanford_jar, read=True, no_print=True)

        if not status:
            err_msg = err_msg + msg
            status_flag = False

    return status_flag, err_msg


def non_proc_msg(                               # pylint:disable=R0913,R0914
        rmq, log, cfg, data, subj, r_key):

    """Function:  non_proc_msg

    Description:  Process non-processed messages.

    Arguments:
        (input) rmq -> RabbitMQ class instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (input) data -> Body of message that was not processed
        (input) subj -> Email subject line
        (input) r_key -> Routing key for message

    """

    log.log_info(
        f"non_proc_msg:  Processing failed message: Routing Key: {r_key}")
    frm_line = getpass.getuser() + "@" + socket.gethostname()
    rdtg = datetime.datetime.now()
    msecs = str(int(rdtg.microsecond / 100))
    dtg = datetime.datetime.strftime(rdtg, "%Y-%m-%d_%H:%M:%S") + "." + msecs
    f_name = rmq.exchange + "_" + r_key + "_" + dtg + ".txt"
    f_path = os.path.join(cfg.message_dir, f_name)
    subj = "rmq_metadata: " + subj
    line1 = f"RabbitMQ message was not processed due to: {subj}"
    line2 = f"Exchange: {rmq.exchange}, Routing Key: {r_key}"
    line3 = \
        f"Check log file: {cfg.log_file} near timestamp: {dtg} for more" \
        f" information."
    line4 = f"Body of message saved to: {f_path}"

    if cfg.to_line:
        log.log_info(f"Sending email to: {cfg.to_line}")
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
    log.log_err(line4)
    gen_libs.write_file(f_path, data=data, mode="w")


def process_msg(rmq, log, cfg, method, body):

    """Function:  process_msg

    Description:  Process message from RabbitMQ queue.

    Arguments:
        (input) rmq -> RabbitMQ class instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (input) method -> Delivery properties
        (input) body -> Message body

    """

    r_key = method.routing_key
    queue = None
    log.log_info(
        f"process_msg:  Processing message body from Routing Key: {r_key}")

    for item in cfg.queue_list:

        if item["routing_key"] == r_key:
            queue = item

            if queue["archive"] and cfg.archive_dir:
                rdtg = datetime.datetime.now()
                msecs = str(int(rdtg.microsecond / 100))
                dtg = datetime.datetime.strftime(rdtg, "%Y-%m-%d_%H:%M:%S") + \
                    "." + msecs
                f_name = rmq.exchange + "_" + queue["routing_key"] + "_" + \
                    dtg + ".body"
                f_path = os.path.join(cfg.archive_dir, f_name)
                log.log_info(f"process_msg:  Archiving message to: {f_path}")
                gen_libs.write_file(f_path, data=body, mode="w")

            break

    if queue:
        convert_data(rmq, log, cfg, queue, body, r_key)

    else:
        non_proc_msg(rmq, log, cfg, body, "No queue detected", r_key)


def convert_data(                               # pylint:disable=R0913,R0914
        rmq, log, cfg, queue, body, r_key):

    """Function:  convert_data

    Description:  Pre-processing of message and decode the message.

    Arguments:
        (input) rmq -> RabbitMQ class instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (input) queue -> RabbitMQ queue
        (input) body -> Message body
        (input) r_key -> Routing key

    """

    prename = ""
    postname = ""
    ext = ""
    log.log_info("convert_data:  Converting data in message body.")
    rdtg = datetime.datetime.now()
    msecs = str(int(rdtg.microsecond / 100))
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
    log.log_info(f"Starting processing of: {f_name}")
    gen_libs.write_file(t_file, data=body, mode="w")

    if queue["stype"] == "encoded":
        log.log_info("convert_data:  Decoding data in message body.")
        base64.decode(
            io.open(t_file, "rb"),                      # pylint:disable=R1732
            io.open(f_name, "wb"))                      # pylint:disable=R1732
        os.remove(t_file)

    else:
        log.log_info("convert_data:  No encoding setting detected.")
        gen_libs.rename_file(t_filename, f_filename, cfg.tmp_dir)

    status = process_message(queue, cfg, f_name, log)

    if status:
        log.log_info(f"Finished processing of: {f_filename}")

    else:
        log.log_err(f"Extractions failed on: {f_filename}")
        log.log_info("Body of message being saved to a file - see below")
        non_proc_msg(rmq, log, cfg, body, "All extractions failed", r_key)
        os.remove(f_name)
        log.log_info("Cleanup of temporary files completed.")
        log.log_info(f"Finished processing of: {f_filename}")


def read_pdf(filename, log):

    """Function:  read_pdf

    Description:  Extract text from a PDF file using the pypdf module.

    Arguments:
        (input) filename -> PDF file name
        (input) log -> Log class instance
        (output) status -> True|False - successfully extraction of data
        (output) text -> Raw text

    """

    text = ""
    status = True
#    pdf = io.open(filename, "rb")                       # pylint:disable=R1732
    pdf = io.open(filename, "rb")
#    pdfreader = PyPDF2.PdfFileReader(pdf)
    pdfreader = pypdf.PdfReader(pdf)

#    if pdfreader.isEncrypted:
    if pdfreader.is_encrypted:
        log.log_err("read_pdf:  PDF is encrypted.")
        status = False

    else:
        log.log_info("read_pdf:  Extracting data...")
        count = 0
#        num_pages = pdfreader.numPages
        num_pages = pdfreader.get_num_pages()

        while count < num_pages:
#            page = pdfreader.getPage(count)
            page = pdfreader.get_page(count)
            count += 1
#            text += page.extractText()
            text += page.extract_text()

    pdf.close()

    return status, text


def find_tokens(tokenized_text, cfg):

    """Function:  find_tokens

    Description:  Using the Stanford NLP module to classify a list of set of
        tokens.

    Arguments:
        (input) tokenized_text -> List of tokens
        (input) cfg -> Configuration settings module for the program
        (output) categorized_text -> List of categorized tokens

    """

    tokenized_text = list(tokenized_text)
    snt = StanfordNERTagger(cfg.lang_module, cfg.stanford_jar, cfg.encoding)
    categorized_text = snt.tag(tokenized_text)

    return categorized_text


def summarize_data(categorized_text, token_types):

    """Function:  summarize_data

    Description:  Summarize a list of categorized tokens and merging them into
        a single unique list.

    Arguments:
        (input) categorized_text -> List of categorized tokens
        (input) token_types -> List of token types to be accepted
        (output) data_list -> List of summarized categorized tokens

    """

    categorized_text = list(categorized_text)
    token_types = list(token_types)
    data_list = []
    tmp_data = []
    current_type = ""

    for item in categorized_text:
        current_type, data_list, tmp_data = sort_data(
            item, current_type, data_list, tmp_data, token_types)

    else:                                               # pylint:disable=W0120
        if tmp_data:
            data_list = merge_data(data_list, tmp_data)

    return data_list


def sort_data(item, current_type, data_list, tmp_data, token_types):

    """Function:  sort_data

    Description:  Combines a series of same token types into a data set and
        ignores the "O" (OTHER) token type.

    Arguments:
        (input) item -> Single set token
        (input) current_type -> Current token type
        (input) data_list -> List of summarized categorized tokens
        (input) tmp_data -> List of current series of token data
        (input) token_types -> List of token types
        (output) current_type -> Current token type
        (output) data_list -> List of summarized categorized tokens
        (output) tmp_data -> List of current series of token data

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


def merge_data(data_list, tmp_data):

    """Function:  merge_data

    Description:  Adds a series of similar token data into a single string
        and adds the token type and string as set to a list.

    Arguments:
        (input) data_list -> List of summarized categorized tokens
        (input) tmp_data -> List of current series of token data
        (output) data_list -> List of summarized categorized tokens

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


def get_pypdf2_data(f_name, cfg, log):

    """Function:  get_pypdf2_data

    Description:  Tokenize, categorize, summarize the raw data from the PDF
        file extracted using pypdf module.

    Arguments:
        (input) f_name -> PDF file name
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (output) status -> True|False - successfully extraction of data
        (output) final_data -> List of categorized tokens from PDF file

    """

    log.log_info("get_pypdf2_data:  Extracting data using pypdf.")
    final_data = []
    status, rawtext = read_pdf(f_name, log)

    if status:
        log.log_info("get_pypdf2_data:  Running word_tokenizer.")
        tokens = word_tokenize(rawtext)
        log.log_info("get_pypdf2_data:  Finding tokens.")
        categorized_text = find_tokens(tokens, cfg)

        if categorized_text:
            log.log_info("get_pypdf2_data:  Summarizing data")
            final_data = summarize_data(categorized_text, cfg.token_types)

    else:
        log.log_warn("get_pypdf2_data:  Extraction failed.")

    return status, final_data


def create_metadata(metadata, data):

    """Function:  create_metadata2

    Description:  Merge a list of data sets into an existing dictionary based
        on the keys in the dictionary or create new keys in the dictionary
        based on the data set in the list.

    Arguments:
        (input) metadata -> Dictionary of meta-data
        (input) data -> List of data sets
        (output) metadata -> Dictionary of meta-data

    """

    data = list(data)

    for item in data:

        # Create new key.
        if item[1] not in list(metadata.keys()):
            metadata[item[1]] = [item[0]]

        # Check for duplicate entry in dictionary's list.
        elif item[0] not in metadata[item[1]]:
            metadata[item[1]].append(item[0])

    return metadata


def extract_pdf(f_name, log, char_encoding=None):

    """Function:  extract_pdf

    Description:  Extract text from PDF using textract module.

    Arguments:
        (input) f_name -> PDF file name
        (input) log -> Log class instance
        (input) char_encoding -> Character encoding code
        (output) status -> True|False - successfully extraction of data
        (output) text -> Raw text

    """

    status = True
    text = ""

    if char_encoding:

        try:
            log.log_info("extract_pdf:  Extracting data -> set encoding.")
            text = textract.process(f_name, encoding=char_encoding)

        except textract.exceptions.ShellError as msg:
            status = False

            if str(msg).find("Incorrect password") >= 0:
                log.log_err("extract_pdf:  PDF is password protected.")

            else:
                log.log_err("extract_pdf:  Error detected.")
                log.log_err(f"Error Message:  {msg}")

    else:
        try:
            log.log_info("extract_pdf:  Extracting data -> default encoding.")
            text = textract.process(f_name)

        except textract.exceptions.ShellError as msg:
            status = False

            if str(msg).find("Incorrect password") >= 0:
                log.log_err("extract_pdf:  PDF is password protected.")

            else:
                log.log_err("extract_pdf:  Error detected.")
                log.log_err(f"Error Message:  {msg}")

    return status, text


def get_textract_data(f_name, cfg, log):

    """Function:  get_textract_data

    Description:  Process data using the textract module.

    Arguments:
        (input) f_name -> PDF file name
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (output) status -> True|False - successfully extraction of data
        (output) final_data -> List of categorized tokens from PDF file

    """

    log.log_info("get_textract_data:  Extracting data using textract.")
    final_data = []

    # Get character encoding.
    log.log_info("get_textract_data:  Detecting encode in PDF file.")
    status, tmptext = extract_pdf(f_name, log)

    if status:
        suberrstr = "codec can't decode byte"
        char_encoding = None
        status_flag = True
        categorized_text = []
        data = chardet.detect(tmptext)

        if data["confidence"] == 1.0:
            char_encoding = data["encoding"]
            log.log_info(f"get_textract_data:  Detected character encode:"
                         f" {char_encoding}")

        _, rawtext = extract_pdf(f_name, log, char_encoding)
        log.log_info("get_textract_data:  Running word_tokenizer.")

        try:
            tokens = word_tokenize(rawtext)

        except UnicodeDecodeError as msg:
            log.log_warn("get_textract_data:  UnicodeDecodeError detected.")

            if str(msg).find(suberrstr) >= 0 \
               and msg.args[0] in cfg.textract_codes:
                char_encoding = msg.args[0]
                log.log_info(f"get_textract_data:  New encoding code detected:"
                             f" {char_encoding}")
                _, rawtext = extract_pdf(f_name, log, char_encoding)
                log.log_info("get_textract_data:  Re-running word_tokenizer.")
                tokens = word_tokenize(rawtext)

            else:
                log.log_warn("get_textract_data:  No encoding code detected.")
                status_flag = False

        if status_flag:
            log.log_info("get_textract_data:  Finding tokens.")
            categorized_text = find_tokens(tokens, cfg)

        if categorized_text:
            log.log_info("get_textract_data:  Summarizing data.")
            final_data = summarize_data(categorized_text, cfg.token_types)

    else:
        log.log_err("get_textract_data:  Extraction failed.")

    return status, final_data


def pdf_to_string(f_name, log):

    """Function:  pdf_to_string

    Description:  Extract text from PDF using pdfminer module.

    Arguments:
        (input) f_name -> PDF file name
        (input) log -> Log class instance
        (output) status -> True|False - successfully extraction of data
        (output) text -> Raw text

    """

    status = True
    out_string = io.BytesIO()

    with io.open(f_name, "rb") as f_hdlr:
        parser = PDFParser(f_hdlr)

        try:
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, out_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            log.log_info("pdf_to_string:  Extracting data...")

            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        except pdfminer.pdfdocument.PDFPasswordIncorrect:
            log.log_err("pdf_to_string:  PDF is password protected.")
            status = False
            text = ""

    data = out_string.getvalue()
    text = data.replace(".", "")

    return status, text


def get_pdfminer_data(f_name, cfg, log):

    """Function:  get_pdfminer_data

    Description:  Process data using the pdfminer module.

    Arguments:
        (input) f_name -> PDF file name
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (output) status -> True|False - successfully extraction of data
        (output) final_data -> List of categorized tokens from PDF file

    """

    final_data = []
    log.log_info("get_pdfminer_data:  Extracting data using pdfminer.")
    status, rawtext = pdf_to_string(f_name, log)

    if status:
        log.log_info("get_pdfminer_data:  Running word_tokenizer.")
        tokens = word_tokenize(rawtext)
        log.log_info("get_pdfminer_data:  Finding tokens.")
        categorized_text = find_tokens(tokens, cfg)

        if categorized_text:
            log.log_info("get_pdfminer_data:  Summarizing data")
            final_data = summarize_data(categorized_text, cfg.token_types)

    else:
        log.log_err("get_pdfminer_data:  Extraction failed.")

    return status, final_data


def process_message(queue, cfg, f_name, log):

    """Function:  process_message

    Description:  Extract metadata from message.

    Arguments:
        (input) queue -> RabbitMQ queue
        (input) cfg -> Configuration settings module for the program
        (input) f_name -> PDF file name
        (input) log -> Log class instance
        (output) status -> True|False - successfully extraction of data

    """

    status = True
    log.log_info("process_message:  Extracting and processing metadata.")
    dtg = datetime.datetime.strftime(
        datetime.datetime.now(), "%Y-%m-%d_%H:%M:%S")
    metadata = {"FileName": os.path.basename(f_name),
                "Directory": queue["directory"],
                "DateTime": dtg}

    # Use the pypdf module to extract data
    status_pypdf2, final_data = get_pypdf2_data(f_name, cfg, log)

    if status_pypdf2:
        log.log_info("process_message:  Adding metadata from pypdf.")
        metadata = create_metadata(metadata, final_data)

    # Use the textract module to extract data
    status_textract, final_data = get_textract_data(f_name, cfg, log)

    if status_textract:
        log.log_info("process_message:  Adding metadata from textract.")
        metadata = create_metadata(metadata, final_data)

    # Use the pdfminer module to extract data
    status_pdfminer, final_data = get_pdfminer_data(f_name, cfg, log)

    if status_pdfminer:
        log.log_info("process_message:  Adding metadata from pdfminer.")
        metadata = create_metadata(metadata, final_data)

    if status_pypdf2 or status_textract or status_pdfminer:
#       Enter code to save metadata to a file.
        log.log_info(f'process_message:  Moving PDF to: {queue["directory"]}')
        gen_libs.mv_file2(f_name, queue["directory"], os.path.basename(f_name))

    else:
        log.log_err("process_message:  All extractions methods failed.")
        status = False

    return status


def monitor_queue(cfg, log):

    """Function:  monitor_queue

    Description:  Monitor RabbitMQ queue for messages.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance

    """

    def callback(channel, method, properties, body):    # pylint:disable=W0613

        """Function:  callback

        Description:  Process message from RabbitMQ.

        Arguments:
            (input) channel -> Channel properties
            (input) method -> Delivery properties
            (input) properties -> Properties of the message
            (input) body -> Message body

        """

        log.log_info(f"callback:  Processing message with Routing Key:"
                     f" {method.routing_key}")
        process_msg(rmq, log, cfg, method, body)
        log.log_info(
            f"Deleting message with Routing Key: {method.routing_key}")
        rmq.ack(method.delivery_tag)

    log.log_info("monitor_queue:  Initialize monitoring of queues...")

    for queue in cfg.queue_list:
        rmq = rabbitmq_class.RabbitMQCon(
            cfg.user, cfg.japd, cfg.host, cfg.port,
            exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
            queue_name=queue["queue"], routing_key=queue["routing_key"],
            x_durable=cfg.x_durable, q_durable=cfg.q_durable,
            auto_delete=cfg.auto_delete)

        log.log_info(f'Initializing:  Queue: {queue["queue"]}, Routing Key:'
                     f' {queue["routing_key"]}')
        connect_status, err_msg = rmq.create_connection()

        if connect_status and rmq.channel.is_open:
            log.log_info(f'Initialized RabbitMQ node: {queue["queue"]}')

        else:
            log.log_err(f'Initialization failed RabbuitMQ: {queue["queue"]}'
                        f' -> Msg: {err_msg}')

        rmq.drop_connection()

    log.log_info("monitor_queue:  Start monitoring queue...")

    # Connect to first queue as only one connection required
    rmq = rabbitmq_class.RabbitMQCon(
        cfg.user, cfg.japd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=cfg.queue_list[0]["queue"],
        routing_key=cfg.queue_list[0]["routing_key"],
        x_durable=cfg.x_durable, q_durable=cfg.q_durable,
        auto_delete=cfg.auto_delete)

    log.log_info(f"Connection info: {cfg.host}->{cfg.exchange_name}")
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        log.log_info("Connected to RabbitMQ node")

        # Setup the RabbitMQ Consume callback on multiple queues.
        for queue in cfg.queue_list:
            log.log_info(f'Monitoring RabbitMQ Queue: {queue["queue"]},'
                         f' Routing Key: {queue["routing_key"]}')
            rmq.consume(callback, queue=queue["queue"])

        rmq.start_loop()

    else:
        log.log_err(f"Failed to connnect to RabbuitMQ -> Msg: {err_msg}")


def run_program(args, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Set a program lock to prevent other instantiations from running.

    Arguments:
        (input) args -> ArgParser class instance.
        (input) func_dict -> Dict of function calls and associated options

    """

    func_dict = dict(func_dict)
    cfg = gen_libs.load_module(args.get_val("-c"), args.get_val("-d"))
    cfg, status_flag, err_msg = validate_create_settings(cfg)

    if status_flag:
        log = gen_class.Logger(
            cfg.log_file, cfg.log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")
        str_val = "=" * 80
        log.log_info(f"{cfg.host}:{cfg.exchange_name} Initialized")
        log.log_info(f"{str_val}")
        log.log_info(f"Exchange Name:  {cfg.exchange_name}")
        log.log_info("Queue Configuration:")

        for queue in cfg.queue_list:
            log.log_info(f'\tQueue Name:  {queue["queue"]}, Routing Key:'
                         f' {queue["routing_key"]}')

        log.log_info(f"To Email:  {cfg.to_line}")
        log.log_info(f"{str_val}")

        try:
            flavor_id = args.get_val("-y", def_val=cfg.exchange_name)
            prog_lock = gen_class.ProgramLock(sys.argv, flavor_id)

            # Intersect args.args_array & func_dict to determine function call
            for opt in set(args.get_args_keys()) & set(func_dict.keys()):
                func_dict[opt](cfg, log, **kwargs)

            del prog_lock

        except gen_class.SingleInstanceException:
            log.log_warn(f"rmq_metadata lock in place for: {flavor_id}")

        log.log_close()

    else:
        print("Error:  Problem in configuration file or directory setup.")
        print(err_msg)


def main(**kwargs):

    """Function:  main

    Description:  Initializes program-wide variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains options which will be directories and the
            octal permission settings
        func_dict -> dictionary list for the function calls or other options.
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) sys.argv -> Arguments from the command line.
        (input) **kwargs:
            argv_list -> List of arguments from another program.

    """

    sys.argv = list(kwargs.get("argv_list", sys.argv))
    dir_perms_chk = {"-d": 5}
    func_dict = {"-M": monitor_queue}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d", "-y"]

    # Process argument list from command line
    args = gen_class.ArgParser(sys.argv, opt_val=opt_val_list)

    if args.arg_parse2()                                            \
       and not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_require(opt_req=opt_req_list)                   \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk):
        run_program(args, func_dict)


if __name__ == "__main__":
    sys.exit(main())
