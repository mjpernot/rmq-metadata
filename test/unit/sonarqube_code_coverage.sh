#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/_convert_data.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/_process_queue.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/_sort_data.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/create_metadata.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/extract_pdf.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/find_tokens.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/get_pypdf2_data.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/help_message.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/main.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/merge_data.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/monitor_queue.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/non_proc_msg.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/process_msg.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/read_pdf.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/run_program.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/summarize_data.py
coverage run -a --source=rmq_metadata test/unit/rmq_metadata/validate_create_settings.py
coverage run -a --source=daemon_rmq_metadata test/unit/daemon_rmq_metadata/is_active.py
coverage run -a --source=daemon_rmq_metadata test/unit/daemon_rmq_metadata/main.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i

