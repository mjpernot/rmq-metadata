# Python project for processing PDF files in RabbitMQ and extracting meta-data from the PDF files.
# Classification (U)

# Description:
  Python program that processes PDF files from RabbitMQ.  The program will decode the PDF file, extract meta-data from the PDF file, create a JSON object of the meta-data and write to a file.


###  This README file is broken down into the following sections:
 * Features
 * Prerequisites
 * Installation
 * Configuration
 * System Service
 * Running
 * Program Help Function
 * Testing
   - Unit
   - Integration


# Features:
 * Offload PDF file from RabbitMQ and encode PDF file back to the original format.
 * Extract meta-data from the PDF file.
 * Tokenize and classify the extracted meta-data.
 * Summarize the meta-data and convert to a JSON object.
 * Save PDF and JSON metadata to a file.
 * Run the monitor program as a service/daemon.
 * Setup the program up as a service.


# Prerequisites:
  * List of Linux packages that need to be installed on the server.
    - openjdk-8-jdk or better
    - python3-pip
    - python3-devel
    - gcc

  * Stanford Named Entity Recognizer:  Require the use the English language module and Stanford jar.  These are part of the Stanford NER package which can be downloaded from https://nlp.stanford.edu/software/CRF-NER.html#Download site.  Download the "stanford-ner-4.2.0.zip" file with a v4.2.0 or better.
    - Install this in the user's directory who will run this program and will need access to the "english.all.3class.distsim.crf.ser.gz" and "stanford-ner.jar" files.
    - In the config/rabbitmq.py:
      lang_module = "DIRECTORY_PATH/classifiers/english.all.3class.distsim.crf.ser.gz"
      stanford_jar = "DIRECTORY_PATH/stanford-ner.jar"

# Installation:

Install the project using git.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-metadata.git
```

Install/upgrade system modules.

NOTE: Install as the user that will run the program.
WARNING: Create a seperate user for this program if running other programs on the same server.  This is due to version conflict with the six module.

Redhat 8 (Running Python 3.9 and 3.12):

```
python -m pip install --user -r requirements39.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Make the appropriate changes to the RabbitMQ environment.
  * The "user", "japd" and "host" is connection and host information to a RabbitMQ node.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"
      -> Name of the exchange that will be monitored.
    - to_line = "EMAIL_ADDRESS@EMAIL_DOMAIN"
      -> Is the email address/email alias to the RabbitMQ administrator(s) or None if no emails required.
    - port = 5672
      -> RabbitMQ listening port.
    - exchange_type = "direct"
      -> Type of exchange:  direct, topic, fanout, headers
    - x_durable = True
      -> Is exchange durable: True|False
    - q_durable = True
      -> Are queues durable: True|False
    - auto_delete = False
      -> Queues automatically delete message after processing: True|False
    - base_dir = "DIRECTORY_PATH"
      -> Base directory path for message_dir, log_dir, archive_dir, and tmp_dir settings.
    - message_dir = "message_dir"
      -> Is where failed reports/messages are written to.
    - log_dir = "logs"
      -> Is where failed log files are written to.
    - log_file = "rmq_metadata.log"
      -> File name to program log.
      -> Name should be changed to include the exchange name being processed.
    - archive_dir = None
      -> Directory name for archived messages.  
      -> If set to None, then no archiving will take place.
    - tmp_dir = "tmp"
      -> Directory for temporary processing of messages.
    - lang_module = "DIRECTORY_PATH/classifiers/english.all.3class.distsim.crf.ser.gz"
      -> Path and file name to the Stanford NLP language module.
      -> This entry is pointing to the English language module.
      -> Path is available once the nltk module is installed via pip.
    - stanford_jar = "DIRECTORY_PATH/stanford-ner.jar"
      -> Path and file name to the Stanford NLP jar file.
      -> Path is available once the nltk module is installed via pip.
    - encoding = "utf-8"
      -> Encoding set used in the Stanford NLP processing.
      -> Default setting is the utf-8 encoding code.
      -> The utf-8 code will work in most cases, do not recommend changing this value.
    - token_types = ["LOCATION", "PERSON", "ORGANIZATION"]
      -> Categories for the tokens for Stanford NLP and textract.
      -> Do not change unless you understand Stanford NLP and textract modules.
    - textract_codes = ["utf-8", "ascii", "iso-8859-1"]
      -> Encoding values for the textract module.
      -> Do not change unless you understand textract module.
  * The next entry is the queue_list.  This is a list of dictionaries.  Each dictionary within the list is the unique combination of queue name and routing key.  Therefore, each queue name and routing key will have its own dictionary entry within the list.  Make a copy of the dictionary for each combination and modify it for that queue/routing key setup.  Below is a break out of the dictionary.
  *  Recommend the mode, ext, stype settings ARE NOT changed, unless you have a good understanding of the system.
    - "queue": "QUEUE_NAME"
      -> Name of queue to monitor.
    - "routing_key": "ROUTING_KEY"
      -> Name of the routing key for the queue.
      -> NOTE:  A single queue can have multiple routing keys, but each routing key will have it's own dictionary entry.
    - "directory": "DIRECTORY_PATH"
      -> Directory path to where a report will be written to.
    - "prename": ""
      -> A static pre-file name string.
      -> Default: "", nothing will be added to file name.
    - "postname": ""
      -> Default: "", nothing will be added to file name.
      -> A static post-file name string.
    - "mode": "w"|"a"
      -> Write mode to the file: write or append to a file.
      -> Default: "w"
    - "ext": "pdf"
      -> Extension name to the file name.
      -> Default: "pdf"
    - "dtg": True|False
      -> Add a date and time group to the file name.
      -> Format is: YYYYMMDD_YYMMSS, example: 20200619_112012
      -> Default: False, no datetime group will be added to file name.
    - "date":  True|False
      -> Add a date to the file name.
      -> Format is: YYYYMMDD, example: 20200619
      -> Default: False, no date will be added to file name.
    - "stype": "encoded"
      -> States the PDF file is encoded and will require decoding before use.
      -> Default: "encoded"
    - "archive":  True|False
      -> Archive the raw body of the RMQ PDF file.
      -> The archive_dir must be set above for this to take place.
      -> Default:  True.

```
cp config/rabbitmq.py.TEMPLATE config/rabbitmq.py
chmod 600 config/rabbitmq.py
vim config/rabbitmq.py
```

(Optional)  Setup program to be ran as a service.

Modify the service script to change the variables to reflect the environment setup.
  * Change these entries in the rmq_metadata_svc.sh file.
    - BASE_PATH="PYTHON_PROJECT/rmq-metadata"
    - USER_ACCOUNT="USER_NAME"
  * Replace **USER_NAME** with the userid which will execute the daemon and the account must be on the server locally.
  * MOD_LIBRARY is references the configuration file above (e.g. rabbitmq).

```
cp rmq_metadata_svc.sh.TEMPLATE rmq_metadata_svc.sh
vim rmq_metadata_svc.sh
```

Enable program as a service.

```
sudo ln -s PYTHON_PROJECT/rmq-metadata/rmq_metadata_svc.sh /etc/init.d/rmq_metadata
sudo chkconfig --add rmq_metadata
sudo chown USER_NAME config/rabbitmq.py
```


# System Service

Modify the systemctl file to change the variables to reflect the environment setup.
  * Change the working or program directory in rmq-metadata.service file, if installed differently.
  * Change the RabbitMQ configuration file if using a different name.
    - WorkingDirectory=/opt/local/rmq-metadata
    - ExecStart=/opt/local/rmq-sysmon/daemon_rmq_metadata.py -a start -c rabbitmq -d /opt/local/rmq-metadata/config -M
    - ExecStop=/opt/local/rmq-sysmon/daemon_rmq_metadata.py -a start -c rabbitmq -d /opt/local/rmq-metadata/config -M

```
sudo cp rmq-metadata.service /etc/systemd/system
sudo vim /etc/systemd/system/rmq-metadata.service
sudo systemctl enable rmq-metadata.service
```


# Running

### Running as a systemctl.

```
sudo systemctl start rmq-metadata.service
sudo systemctl stop rmq-metadata.service
```

### Running as a daemon.

```
/opt/local/rmq-metadata/daemon_rmq_metadata.py -a start -c rabbitmq -d /opt/local/rmq-metadata/config -M
/opt/local/rmq-metadata/daemon_rmq_metadata.py -a stop -c rabbitmq -d /opt/local/rmq-metadata/config -M
```

### Running from the command line.

```
/opt/local/rmq-metadata/rmq_metadata.py -c rabbitmq -d /opt/local/rmq-metadata/config -M
<Ctrl-C>
```


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
`rmq_metadata.py -h`
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
test/unit/rmq_metadata/unit_test_run.sh
test/unit/daemon_rmq_metadata/unit_test_run.sh
test/unit/rmq_metadata/code_coverage.sh
test/unit/daemon_rmq_metadata/code_coverage.sh
```


# Integration Testing:
  * Note:  This test will require the use of a running RabbitMQ instance.

### Installation:

Install the project using the procedures in the Installation section.

# Configuration:
  * Please note that the integration testing will require access to a rabbitmq system to run the tests.

Make the appropriate changes to the RabbitMQ environment.
  * Change these entries in the rabbitmq.py file.  The "user", "japd", and "host" variables are the connection information to a RabbitMQ node, the other variables use the "Change to" setting values.  If the entry is not listed below then leave with the default value in the file.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"
      -> Change to:  exchange_name = "mail2rmq"
    - to_line = "EMAIL_ADDRESS"
      -> Change to:  to_line = None
    - base_dir = "DIRECTORY_PATH"
      -> Change to: "{Python_Project}/rmq-metadata/test/integration/rmq_metadata"
    - message_dir = "message_dir"
      -> Change to:  "{Python_Project}/rmq-metadata/test/integration/rmq_metadata/message_dir"
    - log_dir = "logs"
      -> Change to:  "{Python_Project}/rmq-metadata/test/integration/rmq_metadata/logs"
    - archive_dir = None
      -> Change to:  archive_dir = "{Python_Project}/rmq-metadata/test/integration/rmq_metadata/archive"
    - tmp_dir = "tmp"
      -> Change to:  archive_dir = "{Python_Project}/rmq-metadata/test/integration/rmq_metadata/tmp"
    - lang_module = "DIRECTORY_PATH/classifiers/english.all.3class.distsim.crf.ser.gz"
      -> Change DIRECTORY_PATH to the location of the NLTP installation.
    - stanford_jar = "DIRECTORY_PATH/stanford-ner.jar"
      -> Change DIRECTORY_PATH to the location of the NLTP installation.
  * Have one entry in the queue_list list:
    - "queue": "QUEUE_NAME",
      -> Change to "queue": "mail2rmq_file",
    - "routing_key": "ROUTING_KEY",
      -> Change to "routing_key": "mail2rmq_file",
    - "directory": "DIR_PATH",
      -> Change to "directory": "{Python_Project}/rmq-metadata/test/integration/rmq_metadata/final_data",

```
cp config/rabbitmq.py.TEMPLATE test/integration/rmq_metadata/rabbitmq.py
chmod 600 test/integration/rmq_metadata/rabbitmq.py
vim test/integration/rmq_metadata/rabbitmq.py
```


### Testing:

```
test/integration/rmq_metadata/integration_test_run.sh
test/integration/rmq_metadata/code_coverage.sh
```

