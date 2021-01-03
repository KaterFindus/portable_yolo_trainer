#!/bin/bash
echo "$1"
echo 'Python version:'
python3 --version

# Navigate to source path
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${SOURCE_DIR}" # is important for the log file to end up at the right place.

./restore_backup_makefile.py


# Activate virtual environment
echo 'Activating virtual environment.'
source venv/bin/activate

# Run .py script
echo 'Executing setup_darknet.py.'
if [[ "$1" = "skipmake" ]]
then ./setup_darknet.py skipmake
else ./setup_darknet.py
fi

./start_training.bash

# echo "Starting testing"
# ./start_testing.bash