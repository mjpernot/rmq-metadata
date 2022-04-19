#!/bin/bash
# Integration testing program for the rmq_metadata.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Integration test:  rmq_metadata.py"
test/integration/rmq_metadata/convert_data.py
test/integration/rmq_metadata/extract_pdf.py
test/integration/rmq_metadata/find_tokens.py
test/integration/rmq_metadata/get_pdfminer_data.py
test/integration/rmq_metadata/get_pypdf2_data.py
test/integration/rmq_metadata/get_textract_data.py
test/integration/rmq_metadata/main.py
test/integration/rmq_metadata/non_proc_msg.py
test/integration/rmq_metadata/pdf_to_string.py
test/integration/rmq_metadata/process_message.py
test/integration/rmq_metadata/process_msg.py
test/integration/rmq_metadata/read_pdf.py
test/integration/rmq_metadata/run_program.py
test/integration/rmq_metadata/sort_data.py
test/integration/rmq_metadata/summarize_data.py
test/integration/rmq_metadata/validate_create_settings.py
test/integration/rmq_metadata/validate_files.py

