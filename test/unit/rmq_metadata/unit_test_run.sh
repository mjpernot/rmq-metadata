#!/bin/bash
# Unit testing program for the rmq_metadata.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  rmq_metadata.py"
test/unit/rmq_metadata/_convert_data.py
test/unit/rmq_metadata/_process_queue.py
test/unit/rmq_metadata/help_message.py
test/unit/rmq_metadata/main.py
test/unit/rmq_metadata/monitor_queue.py
test/unit/rmq_metadata/non_proc_msg.py
test/unit/rmq_metadata/process_msg.py
test/unit/rmq_metadata/read_pdf.py
test/unit/rmq_metadata/run_program.py
test/unit/rmq_metadata/validate_create_settings.py

