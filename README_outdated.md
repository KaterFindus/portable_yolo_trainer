# Portable YOLO trainer

ToDo: add log file info.

## Important: overwriting behaviour
`train.txt`, `test.txt`, `data.data` and `classes.names` will be **overwritten** every time 
`main.sh` is run.
Weights created by a possible previous run under the folder 'backup' will also be overwritten
Make sure to copy them elsewhere if you want to keep them.  

## How to use
- Make sure your labeled data is in the folder *training_set* according to the
 requirements listed further below.
- in a terminal window, run  
`./main.sh`  
(you will have to provide the path if the terminal is not run in the main folder (*portable_yolo_trainer*).)
- If file is not executable, run  
`chmod +x`  
on the file (and possibly also on `start_training.sh` and `setup_darknet.py`.

## Description
This set of scripts allows you to train a YOLO descriptor from this folder.

It uses pre-trained weights that are stored in the folder 'weights'.    
The images that have been prepared for training (e.g. using labelImg or similar software)
have to be placed in the folder 'training_set', together with the corresponding .txt files
(containing the bounding box information for each image file) as well as the `classes.txt`
file that has been created during labeling. 
The files `train.txt`, `test.txt`, `classes.names`, `portable_yolo_trainer_TRAIN.cfg`, 
`portable_yolo_trainer_TEST.cfg` and `data.data` will be created/overwritten
each time by `setup_darknet.py`.  
The weights that are being created during training will be overwritten too, unless training
is specified to continue using specific old weights.  

If you have accidentally deleted parts of the *darknet* folder, you can rebuild it by unpacking
the file `darknet.tar.Z`.

## Requirements
Python 3+ needs to be installed. 

## Settings
The settings can be adjusted at the top of the file `setup_darknet.py`

## Content requirements for folder *training_set*
Make sure that the folder 'training_set' contains nothing except:  

- image files that are to be used for training/testing
- corresponding .txt files (one per each image file)
- file `classes.txt`
- file `train.txt`\*
- file `test.txt`\*
- file `classes.names`\*
- file `data.data`\*  
- file `portable_yolo_trainer_TRAIN.cfg`\*
- file `portable_yolo_trainer_TEST.cfg`\*

\* *Optional. Will be created or overwritten by* `main.sh` *(and thereby* `setup_darknet.py` and `start_training.sh`*)*

### Example contents of folder *training_set* before running `main.sh`:
`classes.txt`  
`image_0001.tif`  
`image_0001.txt`  
`image_0002.tif`  
`image_0002.txt`  
`...`  
`...`  
`image_6344.tif`  
`image_6344.txt`  


## Directory structure

portable_yolo_trainer/  
    darknet/  
       - ⊢ 3rdparty/  
       - ⊢ backup/ (*stores weights generated during training. will be created on first run*)  
       - ⊢ build/  
       - ⊢ cfg/  
       - ⊢ cmake/  
       - ⊢ data/  
       - ⊢ include/  
       - ⊢ results/  
       - ⊢ scrips/  
       - ⊢ src/  
       - ⊢ build.ps1  
       - ⊢ build.sh  
       - ⊢ CMakeLists.txt  
       - ⊢ darknet_images.py  
       - ⊢ darknet_video.py  
       - ⊢ darknet.py  
       - ⊢ DarknetConfig.cmake.in  
       - ⊢ image_yolov3.sh  
       - ⊢ image_yolov4.sh  
       - ⊢ json_mjpeg_streams.sh  
       - ⊢ LICENSE  
       - ⊢ Makefile  
       - ⊢ net_cam_v3.sh  
       - ⊢ net_cam_v4.sh  
       - ⊢ README.md  
       - ⊢ video_yolov3.sh  
       - ⊢ video_yolov4.sh  
    - training_set/
        - *place image files here*
        - *place corresponding .txt files here*
        - *place 'classes.txt' file here*
    - venv/
    - weights/
    - darknet.tar.Z
    - main.sh
    - README.md  
    - setup_darknet.py
    - start_training.sh
