# Python project for processing PDF files in RabbitMQ and extracting meta-data from the PDF files.
# Classification (U)

# Description:
  Python program that processes PDF files from RabbitMQ.  The program will decode the PDF file, extract meta-data from the PDF file, create a JSON object of the meta-data and insert the data into a Mongo database.


###  This README file is broken down into the following sections:
 * Features
 * Prerequisites
   - FIPS Environment
 * Installation
 * Configuration
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
 * Insert JSON object into a Mongo database and save PDF to a Linux file.
 * Run the monitor program as a service/daemon.
 * Setup the program up as a service.


# Prerequisites:
  * List of Linux packages that need to be installed on the server.
    - openjdk-8-jdk
    - Centos 7 (Running Python 2.7):
      -> python-pip
      -> python-devel
    - Redhat 8 (Running Python 3.6):
      -> python3-pip
      -> python3-devel

  * FIPS Environment:  If operating in a FIPS 104-2 environment, this package will require at least a minimum of pymongo==3.8.0 or better.  It will also require a manual change to the auth.py module in the pymongo package.  See below for changes to auth.py.  In addition, other modules may require to have the same modification as the auth.py module.  If a stacktrace occurs and it states "= hashlib.md5()" is the problem, then note the module name "= hashlib.md5()" is in and make the same change as in auth.py:  "usedforsecurity=False".
    - Locate the auth.py file python installed packages on the system in the pymongo package directory.
    - Edit the file and locate the \_password_digest function.
    - In the \_password_digest function there is an line that should match: "md5hash = hashlib.md5()".  Change it to "md5hash = hashlib.md5(usedforsecurity=False)".
    - Lastly, it will require the configuration file entry auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.

# Installation:

Install the project using git.
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-metadata.git
cd rmq-metadata
```

Install/upgrade system modules.

Centos 7 (Running Python 2.7):
```
sudo pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

Centos 7 (Running Python 2.7):
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
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
  * Mongo configuration file name.
    - mongo_cfg = "mongo"
      -> Do not change the default unless changing the mongo configuration file name in the next section.
      -> Only requires the base name of the file name.
    - mongo = None
      -> Mongo configuration instance.
      -> For internal use.  Do not change.

```
cd config
cp rabbitmq.py.TEMPLATE rabbitmq.py
vim rabbitmq.py
chmod 600 rabbitmq.py
```

Create Mongodb configuration file.  Make the appropriate change to the environment.
  * Make the appropriate changes to connect to a Mongo database.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"

  * Change these entries only if required:
    - port = 27017
    - conf_file = None
    - auth = True
    - auth_db = "admin"
    - auth_mech = "SCRAM-SHA-1"
    - use_arg = True
    - use_uri = False

  * Notes for auth_mech configuration entry:
    - NOTE 1:  SCRAM-SHA-256 only works for Mongodb 4.0 and better.
    - NOTE 2:  FIPS 140-2 environment requires SCRAM-SHA-1 or SCRAM-SHA-256.
    - NOTE 3:  MONGODB-CR is not supported in Mongodb 4.0 and better.

  * If connecting to a Mongo replica set, otherwise set to None.
    - repset = "REPLICA_SET_NAME"
    - repset_hosts = "HOST_1:PORT, HOST_2:PORT, ..."
    - db_auth = "AUTHENTICATION_DATABASE"

  * If using SSL connections then set one or more of the following entries.  This will automatically enable SSL connections. Below are the configuration settings for SSL connections.  See configuration file for details on each entry:
    - ssl_client_ca = None
    - ssl_client_key = None
    - ssl_client_cert = None
    - ssl_client_phrase = None

  * FIPS Environment for Mongo:  If operating in a FIPS 104-2 environment, this package will require at least a minimum of pymongo==3.8.0 or better.  It will also require a manual change to the auth.py module in the pymongo package.  See below for changes to auth.py.
    - Locate the auth.py file python installed packages on the system in the pymongo package directory.
    - Edit the file and locate the "_password_digest" function.
    - In the "\_password_digest" function there is an line that should match: "md5hash = hashlib.md5()".  Change it to "md5hash = hashlib.md5(usedforsecurity=False)".
    - Lastly, it will require the Mongo configuration file entry auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.

  * Set the database and collection names where the data will be inserted into.
    - dbs = "DATABASE"
    - tbl = "TABLE"

```
cp mongo.py.TEMPLATE mongo.py
vim mongo.py
chmod 600 mongo.py
```

(Optional)  Setup program to be ran as a service.

Modify the service script to change the variables to reflect the environment setup.
  * Change these entries in the rmq_metadata_svc.sh file.
    - BASE_PATH="PYTHON_PROJECT/rmq-metadata"
    - USER_ACCOUNT="USER_NAME"
  * Replace **PYTHON_PROJECT** with the baseline path of the python program.
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


# Running
  * Replace **{Python_Project}** with the baseline path of the python program.

### Running as a service.
  * Starting the service.

```
service rmq_metadata start
```

  * Stopping the service.

```
service rmq_metadata stop
```

### Running as a daemon.
  * Starting the daemon.

```
{Python_Project}/rmq-metadata/daemon_rmq_metadata.py -a start -c rabbitmq -d {Python_Project}/rmq-metadata/config -M
```

  * Stopping the daemon.

```
{Python_Project}/rmq-metadata/daemon_rmq_metadata.py -a stop -c rabbitmq -d {Python_Project}/rmq-metadata/config -M
```

### Running from the command line.
  * Stating the program.

```
{Python_Project}/rmq-metadata/rmq_metadata.py -c rabbitmq -d {Python_Project}/rmq-metadata/config -M
```

  * Stopping the program.

```
<Ctrl-C>
```


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
`{Python_Project}/rmq-metadata/rmq_metadata.py -h`
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
cd {Python_Project}/rmq-metadata
test/unit/rmq_metadata/unit_test_run.sh
test/unit/daemon_rmq_metadata/unit_test_run.sh
```

### Code coverage:

```
cd {Python_Project}/rmq-metadata
test/unit/rmq_metadata/code_coverage.sh
test/unit/daemon_rmq_metadata/code_coverage.sh
```


# Integration Testing:
  * Note:  This test will require the use of a running RabbitMQ instance and a Mongo database or replica set.

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
cd test/integration/rmq_metadata
cd config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
vim rabbitmq.py
chmod 600 rabbitmq.py
```

Make the appropriate changes to the Mongo environment.
  * Change these entries in the mongo.py file.  The "user", "japd", "host", and "name" variables are the connection information to a Mongo database, the other variables use the "Change to" settings.

    - user = "USER"
    - japd = "PSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"
    - port = 27017
    - conf_file = None
    - auth = True
    - auth_db = "admin"
    - auth_mech = "SCRAM-SHA-1"
    - use_arg = True
    - use_uri = False

  * If connecting to a Mongo replica set:
    - repset = "REPLICA_SET_NAME"
    - repset_hosts = "HOST_1:PORT, HOST_2:PORT, ..."
    - db_auth = "AUTHENTICATION_DATABASE"

```
cp ../../../../config/mongo.py.TEMPLATE mongo.py
vim mongo.py
chmod 600 mongo.py
```

### Testing:

```
cd {Python_Project}/rmq-metadata
test/integration/rmq_metadata/integration_test_run.sh
```

### Code coverage:

```
cd {Python_Project}/rmq-metadata
test/integration/rmq_metadata/code_coverage.sh
```

