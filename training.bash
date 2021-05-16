#!/bin/bash
# Arguments: first optional argument "skipmake" to skip rebuilding the darknet with the settings provided in
#             setup_darknet.py
#            second optional argument: path to weights file to continue training with.
echo "$# arguments were provided"
for arg in "$@"
do
  echo "$arg"
done


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
if [[ "$1" = "skipmake" ]]; then
  echo "Make darknet will be skipped."
  echo 'Executing setup_darknet.py.'
  ./setup_darknet.py skipmake
else
  echo 'Executing setup_darknet.py.'
  ./setup_darknet.py
fi


echo "Starting training."

# Check if there are two arguments provided
if [ $# -eq 2 ]; then
  echo "Continuing using previously trained weights."
  echo "Weights used:"
  echo $2
  ./Data/darknet/darknet detector train "$data" "$train_cfg" "$2" -gpus 0
else
  echo "Starting training from scratch."
  # Structure: ./darknet detector <train or test> <.data file> <.cfg file> <-dont_show flag>
  ./Data/darknet/darknet detector train "$data" "$train_cfg" -gpus 0
fi

