#!/usr/bin/env bash

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
data="${SOURCE_DIR}/Data/darknet/cfg/portable_yolo_trainer.data"
test_cfg="${SOURCE_DIR}/Data/darknet/cfg/portable_yolo_trainer_TEST.cfg"

cd "${SOURCE_DIR}"

echo "Starting testing."
./Data/darknet detector test "$data" "$test_cfg"
