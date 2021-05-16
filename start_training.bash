#!/usr/bin/env bash

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
data="${SOURCE_DIR}/Data/darknet/cfg/portable_yolo_trainer.data"
train_cfg="${SOURCE_DIR}/Data/darknet/cfg/portable_yolo_trainer_TRAIN.cfg"

cd "${SOURCE_DIR}"

# Run YOLO training
# Structure: ./darknet detector <train or test> <.data file> <.cfg file> <-dont_show flag>
echo "Starting training."
./Data/darknet/darknet detector train "$data" "$train_cfg" -dont_show -gpus 0

# To continue using already calculated weights from a previous run:
# ./Data/darknet/darknet detector train "$data" "$train_cfg" ./Data/darknet/backup/ -dont_show


