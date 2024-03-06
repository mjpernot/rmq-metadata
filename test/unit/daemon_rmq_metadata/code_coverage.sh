#!/bin/bash
# Unit test code coverage for daemon_rmq_metadata.py module.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=daemon_rmq_metadata test/unit/daemon_rmq_metadata/main.py 
coverage run -a --source=daemon_rmq_metadata test/unit/daemon_rmq_metadata/is_active.py 

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
 
