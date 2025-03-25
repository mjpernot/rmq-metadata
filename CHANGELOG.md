# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.1.8] - 2025-03-21
Breaking changes

- Removed support for Python 2.7.
- Add pre-header check on allowable Python versions to run.
- Updated pymongo==4.10.1
- Updated urllib3==1.26.20
- Added certifi==2024.12.14
- Updated rabbitmq-lib to v2.3.0
- Updated mongo-lib to v4.5.1
- Updated python-lib to v4.0.0

### Changed
- Refactored open file command and added "encoding" argument to open() command.
- Replaced dict() with {} and list() with [].
- Converted strings to f-strings.
- Documentation changes.


## [0.1.7] - 2024-11-12
- Updated Pillow==8.4.0 for Python 3.
- Updated PyPDF2==3.0.1 for Python 3.
- Updated distro==1.9.0 for Python 3.
- Added idna==2.10 for Python 3.
- Updated pika==1.3.1 for Python 3.
- Updated psutil==5.9.4 for Python 3.
- Updated requests==2.25.0 for Python 3.
- Updated urllib3==1.26.19 for Python 3.
- Added six==1.12.0 for Python 3.
- Added joblib==1.1.1 for Python 3.
- Added tqdm==4.67.0 for Python 3.
- Added click==8.1.7 for Python 3.
- Added typing-extensions==4.12.2 for Python 3.
- Added regex==2023.8.8 for Python 3.
- Updated nltk==3.6.7 for Python 3.
- Added pycryptodome==3.21.0 for Python 3.
- Added SpeechRecognition==3.8.1 for Python 3.
- Added sortedcontainers==2.4.0 for Python 3.
- Added pytz==2024.2 for Python 3.
- Added docx2txt==0.8 for Python 3.
- Added argcomplete==1.10.0 for Python 3.
- Added xlrd==1.2.0 for Python 3.
- Added tzlocal==1.5.1 for Python 3.
- Added python-pptx==0.6.18 for Python 3.
- Added olefile==0.46 for Python 3.
- Added imapclient==2.1.0 for Python 3.
- Added EbookLib==0.17.1 for Python 3.
- Added beautifulsoup4==4.8.0 for Python 3.
- Added extract-msg==0.23.1 for Python 3.
- Updated mongo-lib to v4.3.3
- Updated python-lib to v3.0.8
- Updated rabbitmq-lib to v2.2.7

### Deprecated
- Support for Python 2.7


## [0.1.6] - 2024-09-27
- Updated pymongo==4.1.1 for Python 3.6
- Updated simplejson=3.13.2 for Python 3
- Updated python-lib to v3.0.5
- Updated mongo-lib to v4.3.2


## [0.1.5] - 2024-08-07
- Updated simplejson==3.13.2
- Updated requests==2.25.0
- Added certifi==2019.11.28
- Added idna==2.10

### Changed
- Updates to requirements.txt.


## [0.1.4] - 2024-07-31
- Set urllib3 to 1.26.19 for Python 2 for security reasons.
- Updated rabbitmq-lib to v2.2.4

### Changed
- main: Removed parsing from gen_class.ArgParser call and called arg_parse2 as part of "if" statement.


## [0.1.3] - 2024-04-23
- Updated mongo-lib to v4.3.0
- Added TLS capability for Mongo
- Set pymongo to 3.12.3 for Python 2 and Python 3.

### Changed
- Set pymongo to 3.12.3 for Python 2 and Python 3.
- config/mongo.py.TEMPLATE: Added TLS entries.
- Documentation updates.


## [0.1.2] - 2024-03-05
- Updated to work in Red Hat 8
- Updated rabbitmq-lib to v2.2.3
- Updated mongo-lib to v4.2.9
- Updated python-lib to v3.0.3

### Changed
- daemon_rmq_metadata: Replaced arg_parser.arg_parse2 with gen_class.ArgParser class.
- daemon_rmq_metadata.main:  Removed gen_libs.get_inst call.
- rmq_metadata: main, run_program: Removed gen_libs.get_inst call.
- rmq_metadata.main: Replaced args.get_args with args in gen_libs.help_func parameter list.
- Set simplejson to 3.12.0 for Python 3.
- Set chardet to 3.0.4 for Python 2.
- Documentation updates.


## [0.1.1] - 2022-12-06
- Updated to work in Python 3 too
- Upgraded python-lib to v2.9.4
- Upgraded rabbitmq-lib to v2.2.1
- Upgraded mongo-lib to v4.2.2

### Changed
- Converted imports to use Python 2.7 or Python 3.
- create_metadata: Changed output of dictionary keys call to a list.
- non_proc_msg, process_msg, convert_data: Converted division results to an integer.
- pdf_to_string:  Fully qualified BytesIO call.
- pdf_to_string, read_pdf, convert_data: Changed open() to io.open().


## [0.1.0] - 2020-10-05
- Alpha release
- Upgrade Rabbitmq-lib module to v2.2.0
- Upgrade Python-lib module to v2.9.3

### Fixed
- \_process_queue:  Added status check on Mongo data insert command.
- validate_create_settings:  Incorrect setting of tmp_dir if not absolute path setting.

### Changed
- main, run_program: Replaced the use of arg_parser (args_array) with gen_class.ArgParser class (args).
- Renamed \_validate_files to validate_files.
- Renamed \_sort_data to sort_data.
- Renamed \_process_queue to process_message.
- Renamed \_convert_data to convert_data.
- config/rabbitmq.py.TEMPLATE: Added entry to connect to RabbitMQ cluster, base_dir entry and reformatted the file.
- config/mongo.py.TEMPLATE: Added SSL connection entries and auth_db entry and reformatted the file and removed use_arg and use_uri entries.
- validate_create_settings:  Moved base_dir to configuration file entry: cfg.base_dir.
- run_program:  Determine whether to use exchange name or -y option for program lock flavor id.
- main:  Add -y option for program lock option to have flavor id capability.
- non_proc_msg:  Changed error message to point to log file entries.
- \_convert_data:  Changed to handle extraction or insertion failure.
- Removed an unnecessary \*\*kwargs from function paramters list.
- \_process_queue:  Removed body and r_key arguments - no longer required.
- Documentation updates.

### Removed
- Removed non-used module libraries.


## [0.0.3] - 2020-10-01
### Added
- get_pdfminer_data:  Process data using the pdfminer module.
- pdf_to_string:  Extract text from PDF using pdfminer module.

### Changed
- \_convert_data:  Check and process status return from \_process_queue function.
- get_textract_data, get_pypdf2_data, \_process_queue:  Check status of extractions and return status to calling function.
- extract_pdf, read_pdf:  Added check to see if PDF is encrypted and return status of extraction.


## [0.0.2] - 2020-09-29
### Added
- \_validate_files:  Validates the file entries in the configuration file.

### Changed
- \_process_queue:  Changed format of metadata dictionary to break FileName into directory path and file name.
- validate_create_settings:  Added call to \_validate_files function.
- config/rabbitmq.py.TEMPLATE:  Removed dtg and date entries from queue_list.
- Documentation updates.


## [0.0.1] - 2020-09-11
- Initial pre-alpha release.

