#!/usr/bin/env bash

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
data="${SOURCE_DIR}/darknet/cfg/portable_yolo_trainer.data"
train_cfg="${SOURCE_DIR}/darknet/cfg/portable_yolo_trainer_TRAIN.cfg"
cd "${SOURCE_DIR}"

# Run YOLO training
# Structure: ./darknet detector <train or test> <.data file> <.cfg file> <-dont_show flag>
echo "Starting training."
./darknet/darknet detector train "$data" "$train_cfg" -dont_show -gpus 0

# To continue using already calculated weights from a previous run:
# ./darknet/darknet detector train "$data" "$train_cfg" <path-to-previous-weights> -dont_show


