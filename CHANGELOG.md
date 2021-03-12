# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.1.0] - 2020-10-05
### Fixed
- validate_create_settings:  Incorrect setting of tmp_dir if not absolute path setting.

### Changed
- config/mongo.py.TEMPLATE:  Reformatted the Mongo configuration file.
- config/rabbitmq.py.TEMPLATE:  Reformatted the RabbitMQ configuration file.
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
- extract_pdf:  Added check to see if PDF is encrypted and return status of extraction.
- read_pdf:  Added check to see if PDF is encrypted and return status of extraction.


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

