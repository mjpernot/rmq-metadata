# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.1.0] - 2020-10-05
- Alpha release.
- Upgrade Rabbitmq-lib module to v2.0.0.

### Fixed
- \_process_queue:  Added status check on Mongo data insert command.
- validate_create_settings:  Incorrect setting of tmp_dir if not absolute path setting.

### Changed
- Renamed \_validate_files to validate_files.
- Renamed \_sort_data to sort_data.
- Renamed \_process_queue to process_message.
- Renamed \_convert_data to convert_data.
- config/rabbitmq.py.TEMPLATE: Added entry to connect to RabbitMQ cluster, base_dir entry and reformatted the file.
- config/mongo.py.TEMPLATE: Added SSL connection entries and auth_db entry and reformatted the file.
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

