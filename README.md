# Python project for processing PDF files in RabbitMQ and extracting meta-data from the PDF files.
# Classification (U)

# Description:
  Python program that processes PDF files from RabbitMQ.  The program will decode the PDF file, extract meta-data from the PDF file, create a JSON object of the meta-data and insert the data into a Mongo database.


###  This README file is broken down into the following sections:
 * Features
 * Prerequisites
 * Installation
 * Configuration
 * Running
 * Program Help Function
 * Testing
   - Unit
   - Integration (Not yet implemented)
   - Blackbox (Not yet implemented)


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
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/gen_class
    - lib/arg_parser
    - lib/gen_libs
    - rabbit_lib/rabbitmq_class
    - mongo_lib/mongo_libs


# Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-metadata.git
cd rmq-metadata
chmod 777 logs message_dir tmp
```

Install/upgrade system modules.

```
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create RabbitMQ configuration file.

Make the appropriate changes to the RabbitMQ environment.
  * The "user", "japd" and "host" is connection and host information to a RabbitMQ node.
    - user = "USER"
    - japd = "PASSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"
      -> Name of the exchange that will be monitored.
    - to_line = "EMAIL_ADDRESS"|None
      -> Is the email address/email alias to the RabbitMQ administrator(s) or None if no emails required.
    - message_dir = "DIRECTORY_PATH/message_dir"
      -> Is where failed reports/messages are written to.
    - log_dir = "DIRECTORY_PATH/logs"
      -> Is where failed log files are written to.
    - archive_dir = "DIRECTORY_PATH/archive"|None
      -> Directory name for archived messages.  
      -> If set to None, then no archiving will take place.
  * Do not change these unless you are familar with RabbitMQ.
    - port = 5672
    - exchange_type = "direct"
    - x_durable = True
    - q_durable = True
    - auto_delete = False
  * The next entry is the queue_list.  This is a list of dictionaries.  Each dictionary within the list is the unique combination of queue name and routing key.  Therefore, each queue name and routing key will have its own dictionary entry within the list.  Make a copy of the dictionary for each combination and modify it for that queue/routing key setup.  Below is a break out of the dictionary.
  *  Recommend the mode, ext, stype settings are not changed.
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
cd config
cp rabbitmq.py.TEMPLATE rabbitmq.py
vim rabbitmq.py
chmod 600 rabbitmq.py
```

Create Mongo configuration file.

Make the appropriate change to the environment.
  * Make the appropriate changes to connect to a Mongo database.
    - user = "USER"
    - japd = "PASSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"

  * Change these entries only if required:
    - port = 27017
    - conf_file = None
    - auth = True

  * If connecting to a Mongo replica set:
    - repset = "REPLICA_SET_NAME"
    - repset_hosts = "HOST_1:PORT, HOST_2:PORT, ..."
    - db_auth = "AUTHENTICATION_DATABASE"

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
  * Replace **{Python_Project}** with the baseline path of the python program.

```
`{Python_Project}/rmq-metadata/rmq_metadata.py -h`
```


# Testing:

# Unit Testing:

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-metadata.git
cd rmq-metadata
chmod 777 logs message_dir tmp
```

Install/upgrade system modules.

```
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Testing:
  * Replace **{Python_Project}** with the baseline path of the python program.

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

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-metadata.git
cd rmq-metadata
chmod 777 logs message_dir tmp
```

Install/upgrade system modules.

```
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:
  * Please note that the integration testing will require access to a rabbitmq system to run the tests.

Create RabbitMQ configuration file.

Make the appropriate changes to the RabbitMQ environment.
  * Change these entries in the rabbitmq.py file.  The "user", "japd", and "host" variables are the connection information to a RabbitMQ node, the other variables use the "Change to" settings.
    - user = "USER"
    - japd = "PASSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"            -> Change to:  exchange_name = "intr-test"
    - to_line = "EMAIL_ADDRESS"                  -> Change to:  to_line = None
    - message_dir = "DIRECTORY_PATH/message_dir" -> Change to:  message_dir = "message_dir"
    - log_dir = "DIRECTORY_PATH/logs"            -> Change to:  log_dir = "logs"
  * Have one entry in the queue_list list:
    - "queue_name":                              -> Change value to:  "intr-test"
    - "routing_key":                             -> Change value to:  "intr-test"
    - "directory":                               -> Change value to:  "sysmon"
    - "postname":                                -> Change value to:  "\_pkgs"

```
cd test/integration/rmq_metadata
chmod 777 logs message_dir sysmon
cd config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
vim rabbitmq.py
chmod 600 rabbitmq.py
```

### Testing:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/rmq-metadata
test/integration/rmq_metadata/integration_test_run.sh
```

### Code coverage:
```
cd {Python_Project}/rmq-metadata
test/integration/daemon_rmq_metadata/code_coverage.sh
```


# Blackbox Testing:

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rmq-metadata.git
cd rmq-metadata
chmod 777 logs message_dir tmp
```

Install/upgrade system modules.

```
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create RabbitMQ configuration file.

Make the appropriate changes to the RabbitMQ environment.
  * Replace **{PYTHON_PROJECT}** with the baseline path of the python program.
  * Change these entries in the rabbitmq.py file.  The "user", "japd", and "host" variables are the connection information to a RabbitMQ node, the other variables use the "Change to" settings.
    - user = "USER"
    - japd = "PASSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"            -> Change to:  exchange_name = "blackbox-test"
    - to_line = "EMAIL_ADDRESS@DOMAIN_NAME"      -> Change to:  to_line = None
    - message_dir = "DIRECTORY_PATH/message_dir" -> Change to:  message_dir = "{PYTHON_PROJECT}/test/blackbox/rmq_metadata/message_dir"
    - log_dir = "DIRECTORY_PATH/logs"            -> Change to:  log_dir = "{PYTHON_PROJECT}/test/blackbox/rmq_metadata/logs"
  * Have one entry in the queue_list list:
    - "queue_name":                              -> Change value to:  "blackbox-test"
    - "routing_key":                             -> Change value to:  "blackbox-test"
    - "directory":                               -> Change value to:  "{PYTHON_PROJECT}/test/blackbox/rmq_metadata/sysmon"
    - "postname":                                -> Change value to:  "\_pkgs"

```
cd test/blackbox/rmq_metadata
chmod 777 logs message_dir sysmon
cd config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
vim rabbitmq.py
chmod 600 rabbitmq.py
```

### Testing:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/rmq-metadata
test/blackbox/rmq_metadata/blackbox_test.sh
```

