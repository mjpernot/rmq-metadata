#!/bin/bash
# Integration testing program for the rmq_metadata.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Integration test:  rmq_metadata.py"
/usr/bin/python3 test/integration/rmq_metadata/convert_data.py
/usr/bin/python3 test/integration/rmq_metadata/extract_pdf.py
/usr/bin/python3 test/integration/rmq_metadata/find_tokens.py
/usr/bin/python3 test/integration/rmq_metadata/get_pdfminer_data.py
/usr/bin/python3 test/integration/rmq_metadata/get_pypdf2_data.py
/usr/bin/python3 test/integration/rmq_metadata/get_textract_data.py
/usr/bin/python3 test/integration/rmq_metadata/main.py
/usr/bin/python3 test/integration/rmq_metadata/non_proc_msg.py
/usr/bin/python3 test/integration/rmq_metadata/pdf_to_string.py
/usr/bin/python3 test/integration/rmq_metadata/process_message.py
/usr/bin/python3 test/integration/rmq_metadata/process_msg.py
/usr/bin/python3 test/integration/rmq_metadata/read_pdf.py
/usr/bin/python3 test/integration/rmq_metadata/run_program.py
/usr/bin/python3 test/integration/rmq_metadata/sort_data.py
/usr/bin/python3 test/integration/rmq_metadata/summarize_data.py
/usr/bin/python3 test/integration/rmq_metadata/validate_create_settings.py
/usr/bin/python3 test/integration/rmq_metadata/validate_files.py

