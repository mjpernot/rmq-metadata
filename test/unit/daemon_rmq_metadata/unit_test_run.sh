#!/bin/bash
# Unit testing program for the module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  daemon_rmq_metadata.py"
test/unit/daemon_rmq_metadata/is_active.py
test/unit/daemon_rmq_metadata/main.py

