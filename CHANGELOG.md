# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.0.3] - 2020-10-01
### Added
- get_pdfminer_data:  Process data using the pdfminer module.
- pdf_to_string:  Extract text from PDF using pdfminer module.

### Changed
- extract_pdf:  Added check to see if PDF is encrypted and return status of extraction.
- get_pypdf2_data:  Check status of extraction and return status to calling function.
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

