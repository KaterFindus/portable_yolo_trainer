#!/bin/bash
echo "$1"
echo 'Python version:'
python3 --version

# Navigate to source path
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
data="${SOURCE_DIR}/Data/darknet/cfg/portable_yolo_trainer.data"
train_cfg="${SOURCE_DIR}/Data/darknet/cfg/portable_yolo_trainer_TRAIN.cfg"

cd "${SOURCE_DIR}" # is important for the log file to end up at the right place. Later: Is it? Am I not using absolute paths anyway?

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

# Run YOLO training
# Structure: ./darknet detector <train or test> <.data file> <.cfg file> <-dont_show flag>
echo "Starting training."
./Data/darknet/darknet detector train "$data" "$train_cfg" -dont_show -gpus 0

# To continue using already calculated weights from a previous run:
# ./Data/darknet/darknet detector train "$data" "$train_cfg" ./Data/darknet/backup/ -dont_show