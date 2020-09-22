#!/usr/bin/python

import os
import sys
import base64
import datetime

import PyPDF2
import textract
from PyPDF2 import PdfFileReader
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import StanfordNERTagger
import chardet

import lib.gen_libs as gen_libs
import rabbit_lib.rabbitmq_class as rabbitmq_class


def extract_pdf4(filename, char_encoding=None):
    if char_encoding:
        #print("Using: %s for file: %s" % (char_encoding, filename))
        text = textract.process(filename, encoding=char_encoding)
    else:
        #print("using default encoding for file: %s" % (filename))
        text = textract.process(filename)

    return text


def extract_pdf3(filename):
    text = textract.process(filename, encoding="ascii")

    return text


def extract_pdf(filename):
    text = textract.process(filename)

    return text


def read_pdf(filename):
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


def find_tokens(tokenized_text):
    st = StanfordNERTagger(
    '/home/mark.j.pernot/stanford_ner/stanford-ner-4.0.0/classifiers/english.all.3class.distsim.crf.ser.gz',
    '/home/mark.j.pernot/stanford_ner/stanford-ner-4.0.0/stanford-ner.jar',
    encoding='utf-8')
    classified_text = st.tag(tokenized_text)

    return classified_text


def combine_data(data_list, tmp_data):
    data_list = list(data_list)
    tmp_data = list(tmp_data)

    data = tmp_data.pop(0)
    tmp_a = data[0]
    data_type = data[1]

    for item in tmp_data:
        tmp_a = tmp_a + " " + item[0]

    data_list.append((tmp_a, data_type))

    return data_list

        
def simplfy_data(classified_text):
    data_list = []
    data_types = ["LOCATION", "PERSON", "ORGANIZATION"]
    tmp_data = []
    current_type = ""

    for item in classified_text:
        if item[1] == "O":
            current_type = item[1]

            if tmp_data:
                data_list = combine_data(data_list, tmp_data)
                tmp_data = []

        elif item[1] in data_types and item[1] == current_type:
            tmp_data.append(item)

        elif item[1] in data_types:
            if tmp_data:
                data_list = combine_data(data_list, tmp_data)

            tmp_data = []
            tmp_data.append(item)
            current_type = item[1]

    else:
        if tmp_data:
            data_list = combine_data(data_list, tmp_data)

    return data_list            


def monitor_queue(cfg, **kwargs):
    def callback(channel, method, properties, body):
        process_msg(rmq, cfg, method, body)
        rmq.ack(method.delivery_tag)

    for queue in cfg.queue_list:
        rmq = rabbitmq_class.RabbitMQCon(
            cfg.user, cfg.japd, cfg.host, cfg.port,
            exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
            queue_name=queue["queue"], routing_key=queue["routing_key"],
            x_durable=cfg.x_durable, q_durable=cfg.q_durable,
            auto_delete=cfg.auto_delete)
        connect_status, err_msg = rmq.create_connection()

        if connect_status and rmq.channel.is_open:
            print("Initialized RabbitMQ node: %s" % (queue["queue"]))
        else:
            print("Initialization failed RabbuitMQ: %s -> Msg: %s" %
                  (queue["queue"], err_msg))

        rmq.drop_connection()

    rmq = rabbitmq_class.RabbitMQCon(
        cfg.user, cfg.japd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=cfg.queue_list[0]["queue"],
        routing_key=cfg.queue_list[0]["routing_key"],
        x_durable=cfg.x_durable, q_durable=cfg.q_durable,
        auto_delete=cfg.auto_delete)
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        for queue in cfg.queue_list:
            rmq.consume(callback, queue=queue["queue"])

        rmq.start_loop()
    else:
        print("Failed to connnect to RabbuitMQ -> Msg: %s" % (err_msg))


### DONE
def process_msg(rmq, cfg, method, body, **kwargs):
    r_key = method.routing_key
    queue = None

    #print(r_key)
    #print(cfg.queue_list)
    #sys.exit()

    for item in cfg.queue_list:
        if item["routing_key"] == r_key:
            queue = item

            if queue["archive"] and cfg.archive_dir:
                # Must make this an unique name.
                rdtg = datetime.datetime.now()
                msecs = str(rdtg.microsecond / 100)
                dtg = datetime.datetime.strftime(rdtg, "%Y-%m-%d_%H:%M:%S") + \
                      "." + msecs
                f_name = rmq.exchange + "_" + queue["routing_key"] + "_" + \
                         dtg + ".body"
                #f_name = rmq.exchange + queue["routing_key"] + ".body"
                f_path = os.path.join(cfg.archive_dir, f_name)
                gen_libs.write_file(f_path, data=body, mode="w")
            break

    if queue:
        _convert_data(rmq, cfg, queue, body, r_key)
    else:
        non_proc_msg(rmq, cfg, body, "No queue detected", r_key)


### DONE
def non_proc_msg(rmq, cfg, data, subj, r_key, **kwargs):
    f_name = "myfile" + rmq.exchange + r_key + ".txt"
    f_path = os.path.join(cfg.message_dir, f_name)
    #print("RabbitMQ message was not processed due to: %s" % (subj))
    #gen_libs.write_file(f_path, data="Exchange: %s, Routing Key: %s"
    #                    % (rmq.exchange, r_key))
    gen_libs.write_file(f_path, data=data, mode="w")


def _convert_data(rmq, cfg, queue, body, r_key, **kwargs):
    prename = ""
    postname = ""
    ext = ""
    rdtg = datetime.datetime.now()
    msecs = str(rdtg.microsecond / 100)
    dtg = datetime.datetime.strftime(rdtg, "%Y%m%d%H%M%S") + "." + msecs

    t_filename = "tmp_" + rmq.exchange + "_" + r_key + "_" + dtg + ".txt"
    t_file = os.path.join(cfg.tmp_dir, t_filename)

    # Need to check ext, prename, and postname settings in queue_list.
    if queue["prename"]:
        prename = queue["prename"] + "_"

    if queue["postname"]:
        postname = "_" + queue["postname"]

    if queue["ext"]:
        ext = "." + queue["ext"]
    
    f_filename = prename + rmq.exchange + "_" + r_key + "_" + dtg + \
                 postname + ext
    f_name = os.path.join(cfg.tmp_dir, f_filename)

    gen_libs.write_file(t_file, data=body, mode="w")

    if queue["stype"] == "encoded":
        # Can decode string using the following command:
        # decoded_body = base64.decodestring(body)
        # But can textract andPyPDF2 handle a string?
        base64.decode(open(t_file, 'rb'), open(f_name, 'wb'))
        os.remove(t_file)

    else:
        gen_libs.rename_file(t_filename, f_filename, cfg.tmp_dir)

    _process_queue(queue, body, r_key, cfg, rmq, f_name)


def create_metadata(f_name, final_data, final_data2, **kwargs):
    dtg = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M%S")
    metadata = {"filename": f_name,
                "datetime": dtg}

    for item in final_data:
        if item[1] not in metadata.keys():
            metadata[item[1]] = [item[0]]
        elif item[0] not in metadata[item[1]]:
            metadata[item[1]].append(item[0])

    for item in final_data2:
        if item[1] not in metadata.keys():
            metadata[item[1]] = [item[0]]
        elif item[0] not in metadata[item[1]]:
            metadata[item[1]].append(item[0])

    return metadata


def _process_queue(queue, body, r_key, cfg, rmq, f_name, **kwargs):
    #"""
    # Using PyPDF2 process to extract data.
    rawtext = read_pdf(f_name)
    tokens = word_tokenize(rawtext)
    classified_text = find_tokens(tokens)

    if classified_text:
        final_data = simplfy_data(classified_text)

    gen_libs.write_file("mypypdf2_data.txt", data=final_data, mode="w")
    #"""

    #"""
    # Using textract process to extract data.
    suberrstr = "codec can't decode byte"
    available_sets = ["utf-8", "ascii", "iso-8859-1"]
    char_encoding = None
    status = True
    tmptext = extract_pdf4(f_name)
    data = chardet.detect(tmptext)

    if data["confidence"] == 1.0:
        #print("Changing character encoding to: %s" % (data["encoding"]))
        char_encoding = data["encoding"]

    rawtext2 = extract_pdf4(f_name, char_encoding)
    #rawtext2 = extract_pdf(f_name)

    try:
        tokens2 = word_tokenize(rawtext2)
    except UnicodeDecodeError as msg:
        if str(msg).find(suberrstr) >= 0 and msg.args[0] in available_sets:
            char_encoding = msg.args[0]
            rawtext2 = extract_pdf4(f_name, char_encoding)
            tokens2 = word_tokenize(rawtext2)
        else:
            status = False
            non_proc_msg(rmq, cfg, body, "Failed word tokenization", r_key)

    if status:
        classified_text2 = find_tokens(tokens2)

        if classified_text2:
            final_data2 = simplfy_data(classified_text2)

        gen_libs.write_file("mytextract_data.txt", data=final_data2, mode="w")
    #"""

    # Create metadata object.
    metadata = create_metadata(f_name, final_data, final_data2, **kwargs)

    gen_libs.mv_file2(f_name, "./final_data", "myfinalpdf.pdf")
    print(metadata)
    # Insert data into Mongo database here.

def main():
    test_path = "/home/mark.j.pernot/pdf_docs"
    config_path = os.path.join(test_path, "config")
    cfg = gen_libs.load_module("rabbitmq2", config_path)
    monitor_queue(cfg)


if __name__ == "__main__":
    sys.exit(main())





