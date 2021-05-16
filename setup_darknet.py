#!/usr/bin/env python3

# SEEMS TO REQUIRE libopencv-dev (normal linux package, not pip)
"""
This script expects the training data (images as well as associated .txt files) to be in the folder
'training_set'.

ToDo:   Depending on whether GPU is used or not, change NVCC line, and training command (-gpus 0)
ToDo:   extract image extension from img files, don't rely on the setting in this script.
ToDo:   Figure out how to monitor training output and then send a n email once training has reached
        satisfying results.
ToDO:   allow for continuing with already saved weights. overwriting train.txt etc. should not be a problem.
        (do that in start_training.bash and use a -cont argument in main.bash perhaps?
        Better idea: set up a start_training.bash and a cont_training.bash)
ToDo:   create requirements.txt
ToDo:   Maybe use os.scandir() instead of os.listdir()
Regarding image_converter.py:
ToDo:   OR: use only a target image format and use a list of common source file types ['tif', 'png', 'jpg', 'bmp']
        but only copy the images that are already in target format.

"""
import os
import random
import logging
import subprocess
import time
import sys



# --------------   A D J U S T A B L E   S E T T I N G S   ---------------------------------------------------- #
# ToDo: Mavbe put the settings in their own cfg file? Although it might get confusing w/ all the cfg files at some point
# Logging settings


training_proportion = 0.8               # Proportion used for training. Testing: 1 - training_proportion
img_ext = '.jpg'                        # Image extension of the images in the dataset (not all are accepted for
                                        # in training with darknet (tif produces errors, for example).

makefile_settings = {'GPU': 1,          # set GPU=1 and CUDNN=1 to speedup on GPU
                     'CUDNN': 1,        # set GPU=1 and CUDNN=1 to speedup on GPU
                     'CUDNN_HALF': 0,   # set CUDNN_HALF=1 to further speedup 3 x times (Mixed-precision on Tensor
                                        # Cores) GPU: Volta, Xavier, Turing and higher
                     'OPENCV': 1,       # Use OpenCV
                     'DEBUG': 1,        # Build darknet in debug mode
                     'AVX': 0,          # set AVX=1 and OPENMP=1 to speedup on CPU (if error occurs then set AVX=0)
                     'OPENMP': 0,       # set AVX=1 and OPENMP=1 to speedup on CPU (if error occurs then set AVX=0)
                     'LIBSO': 0,
                     'ZED_CAMERA': 0,   # set ZED_CAMERA=1 to enable ZED SDK 3.0 and above
                     'ZED_CAMERA_v2_8': 0}  # set ZED_CAMERA_v2_8=1 to enable ZED SDK 2.X

cfg_settings = {'batch': 32,
                'subdiv': 16,
                'coords': 5,
                'masks': 3}

make_quiet = 1                          # Use 'quiet' mode when (re-)building darknet from Makefile

# -----   E N D   O F   A D J U S T A B L E   S E T T I N G S   --------------------------------------------- #

# Paths and file names
fname_cfg_test = 'portable_yolo_trainer_TEST.cfg'
fname_cfg_train = 'portable_yolo_trainer_TRAIN.cfg'
fname_classes = 'classes.names'
fname_datafile = 'portable_yolo_trainer.data'
fname_logfile = 'log_setup_darknet_' + time.strftime('%Y-%m-%d_%H-%M', time.localtime()) + '.txt'
fname_testing = 'test.txt'
fname_training = 'train.txt'
fpath_source = os.path.realpath(__file__).rpartition('/')[0] + '/'
fpath_dataset = fpath_source + 'Data/training_set/'
fpath_darknet = fpath_source + 'Data/darknet/'
fpath_cfg_test = fpath_darknet + 'cfg/' + fname_cfg_test
fpath_cfg_train = fpath_darknet + 'cfg/' + fname_cfg_train
fpath_datafile = fpath_darknet + 'cfg/'
fpath_logfile = fpath_source + 'Data/log_files/'
fpath_makefile = fpath_darknet + 'Makefile'
fpath_weights_out = fpath_darknet + 'backup'
fpath_weights_pretrained = fpath_source + 'Data/weights/'

logging.basicConfig(filename=(fpath_logfile + fname_logfile), level=logging.DEBUG,
                    format='%(asctime)s [ %(levelname)s ]\t%(message)s')
logging.info('Source: ' + fpath_source)
logging.info('Dataset: ' + fpath_dataset)
logging.info('Darknet: ' + fpath_darknet)
logging.info('Pretrained weights: ' + fpath_weights_pretrained)
logging.info('Makefile: ' + fpath_makefile)
logging.info('.cfg (train): ' + fpath_cfg_train)
logging.info('.cfg (test): ' + fpath_cfg_test)
logging.info('.data file: ' + fpath_datafile)

logging.info('Training proportion: ' + str(training_proportion))


# Creating required files: class.files, train.txt, data.data

"""
This part of the script creates the train.txt and test.txt files that contain the links to the corresponding
image files.
It also creates the 'classes.files' file from the 'classes.txt' file that it expects to find in
the folder 'training_set'.
Test proportion can be adjusted in the settings above.
Image extension type can be adjusted in the settings below.
"""

# Get image paths                           # ToDo: handle different img. exts, but exclude other stuff...
files = sorted(os.listdir(fpath_dataset))
# Exclude excluded files (duh!)
excluded_files = ['classes.txt', fname_classes, fname_testing, fname_training, fname_datafile, ]
files = [name for name in files if not (name in excluded_files)]
# Add main path before
files = [(fpath_dataset + name) for name in files]
# Exclude .txt files
names_img = [name for name in files if name.endswith(img_ext)]

# Make sure there's a .txt file for each IMG file.
names_txt = [name for name in files if name.endswith('.txt')]
assert len(names_img) == len(names_txt), f'IMG and TXT file count does not match. Are all images {img_ext}?'
logging.info('File counts match.')

# Split into train and test set:
# Create random index list
fcount = len(names_img)
rand_index = random.sample(range(fcount), int(fcount * training_proportion))
# Split image files
train_names_img = sorted([names_img[i] for i in rand_index])
test_names_img = sorted(name for name in names_img if name not in train_names_img)
print()  # Give the output some air
print(f'Total img count: {fcount} files.')
print(f'Train/Test ratio: {training_proportion}/{1 - training_proportion}')
print(f'Train set:\t{len(train_names_img)} files.')
print(f'Test set:\t{len(test_names_img)} files.')
logging.info(f'Train/Test ratio: {training_proportion}/{1 - training_proportion}')
logging.info(f'Train set:\t{len(train_names_img)} files.')
logging.info(f'Test set:\t{len(test_names_img)} files.')
print()

# Create files that give YOLO the paths to each file in each set
with open(fpath_dataset + fname_testing, 'w') as f:
    f.writelines([name + '\n' for name in test_names_img])
with open(fpath_dataset + fname_training, 'w') as f:
    f.writelines([name + '\n' for name in train_names_img])
logging.info('Created "test.txt" file in:\t\t' + fpath_dataset)
logging.info('Created "train.txt" file in:\t\t' + fpath_dataset)

# Transform classes.txt to classes.names
with open(fpath_dataset + 'classes.txt', 'r') as f:
    classes = f.readlines()
    with open(fpath_dataset + fname_classes, 'w') as cf:
        cf.writelines(classes)
logging.info('Created "' + fname_classes + '" file in:\t' + fpath_dataset)

# Create labelled_data.data file:
class_count = len(classes)
# class_names = [name for name in classes]
with open(fpath_datafile + fname_datafile, 'w') as f:
    f.write('classes = ' + str(class_count) + '\n')
    f.write('train = ' + fpath_dataset + 'train.txt' + '\n')
    print('train = ' + fpath_dataset + 'train.txt' + '\n')

    f.write('valid = ' + fpath_dataset + 'test.txt' + '\n')
    f.write('names = ' + fpath_dataset + 'classes.names' + '\n')
    f.write('backup = ' + fpath_weights_out)
logging.info('Created "' + fname_datafile + '" file in:\t' + fpath_datafile)


logging.info('Weights will be stored in:\t\t' + os.getcwd() + '/' + fpath_weights_out)



# Preparing the Makefile and (re-) building yolo. #####
"""
Writes specified settings into "Makefile" in the darknet directory and then makes darknet using these settings.
Also copies the .data file specifying the different file locations into darknet's cfg directory.
"""

# Create backup if nonexistent:
if not os.path.isfile(fpath_makefile + '_BACKUP'):
    with open(fpath_makefile, 'r') as rfile:
        with open(fpath_makefile + '_BACKUP', 'w') as wfile:
            wfile.writelines(rfile.readlines())


# Display makefile settings:
print('Makefile settings (can be adjusted in setup_darknet.py):')
longest = 0
for param in list(makefile_settings.keys()):
    if len(param) > longest:
        longest = len(param)
longest += 4
[print('  ' + param.ljust(longest, '.') + str(val)) for param, val in makefile_settings.items()]

with open(fpath_makefile, 'r') as mfile:
    lines = mfile.readlines()

# Change values for Makefile settings
for param, val in makefile_settings.items():
    lines = [line.partition('=')[0] + '=' + str(val) + '\n' if line.startswith(param) else line for line in lines]

# Make sure each line gets a \n again:
lines = [line + '\n' if not line.endswith('\n') else line for line in lines]
logging.info(lines)

# Overwrite file with new adjusted settings
with open(fpath_makefile, 'w') as mfile:
    mfile.writelines(lines)

# (re-)build darknet using the adjusted Makefile
if len(sys.argv) > 1:
    if sys.argv[1] == 'skipmake':
        skip_make = 1
else:
    skip_make = 0

if not skip_make:
    cwd = os.getcwd()
    logging.info('CWD: ' + cwd)
    os.chdir(fpath_darknet)
    print('Rebuilding darknet with above settings.\nThis might take a few minutes. Please be patient.')
    if make_quiet:
        print('Building darknet in quiet mode.')
        subprocess.run(['make'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    else:
        subprocess.run(['make'])
    os.chdir(cwd)
    print('Done rebuilding darknet.')
else:
    print('Skipped make. ---------------------------------------------------------------------- [ WARNING ] ')


# create cfg files for training and testing
"""
Create cfg files for training and for testing (if only one dataset is used)
"""

# Class count
with open(fpath_dataset + 'classes.txt') as classfile:
    classes = [cl.strip() for cl in classfile.readlines()]
class_count = len(classes)

# Calculate max_batches (class_count * 2000, not less than 4000.
if class_count >= 2:
    max_batches = class_count * 2000
else:
    max_batches = 4000

# Calculate number of filters ( (<class count> + <coord count> + 1) * masks )
# filters = (class_count + cfg_settings['coords'] + 1) * cfg_settings['masks']
filters = (class_count + cfg_settings['coords']) * cfg_settings['masks']        # This works, the previous line does not
print('Filters: ' + str(filters))

# Calculate steps (90% of max_batches, 80% of max_batches)
steps = (int(max_batches + 0.9), int(max_batches * 0.8))
print('Steps: ' + str(steps))
print()

# Create new config files with relevant data updated and lines commented/uncommented for training/testing
# ToDo: Define a list with the line numbers below to make it easier to update these manipulations.
# Write cfg file for training
with open(fpath_cfg_train, 'w') as cfg_w:
    with open(fpath_darknet + 'cfg/yolov3.cfg', 'r') as cfg_r:
        lines = cfg_r.readlines()
        # Comment out testing lines
        lines[2], lines[3] = ('# ' + lines[2]), ('# ' + lines[3])
        # Uncomment training lines
        lines[5], lines[6] = lines[5].lstrip('# '), lines[6].lstrip('# ')
        # Overwrite relevant data
        # Batch number
        lines[5] = lines[5].split('=')[0] + '=' + str(cfg_settings['batch']) + '\n'
        # Subdivision number
        lines[6] = lines[6].split('=')[0] + '=' + str(cfg_settings['subdiv']) + '\n'
        # Max batches
        lines[19] = lines[19].split('=')[0] + '=' + str(max_batches) + '\n'
        # Steps
        lines[21] = lines[21].split('=')[0] + '=' + str(steps[0]) + ',' + str(steps[1]) + '\n'
        # Number of filters (updated in each conv. layer above a yolo network)
        lines[602] = lines[602].split('=')[0] + '=' + str(filters) + '\n'
        lines[688] = lines[688].split('=')[0] + '=' + str(filters) + '\n'
        lines[775] = lines[775].split('=')[0] + '=' + str(filters) + '\n'
        # Class counts (updated in the last three yolo layers)
        lines[609] = lines[609].split('=')[0] + '=' + str(class_count) + '\n'
        lines[695] = lines[695].split('=')[0] + '=' + str(class_count) + '\n'
        lines[782] = lines[782].split('=')[0] + '=' + str(class_count) + '\n'

        # Actually update the data:
        cfg_w.writelines(lines)
        print('Created file: ', fpath_cfg_train)

# Write cfg file for testing
with open(fpath_cfg_test, 'w') as cfg_w:
    with open(fpath_darknet + 'cfg/yolov3.cfg', 'r') as cfg_r:
        lines = cfg_r.readlines()

        # Overwrite relevant data
        # Batch number
        lines[5] = lines[5].split('=')[0] + '=' + str(cfg_settings['batch']) + '\n'
        # Subdivision number
        lines[6] = lines[6].split('=')[0] + '=' + str(cfg_settings['subdiv']) + '\n'
        # Max batches
        lines[19] = lines[19].split('=')[0] + '=' + str(max_batches) + '\n'
        # Steps
        lines[21] = lines[21].split('=')[0] + '=' + str(steps[0]) + ',' + str(steps[1]) + '\n'
        # Number of filters (updated in each conv. layer above a yolo network)
        lines[602] = lines[602].split('=')[0] + '=' + str(filters) + '\n'
        lines[688] = lines[688].split('=')[0] + '=' + str(filters) + '\n'
        lines[775] = lines[775].split('=')[0] + '=' + str(filters) + '\n'
        # Class counts (updated in the last three yolo layers)
        lines[609] = lines[609].split('=')[0] + '=' + str(class_count) + '\n'
        lines[695] = lines[695].split('=')[0] + '=' + str(class_count) + '\n'
        lines[782] = lines[782].split('=')[0] + '=' + str(class_count) + '\n'

        # Actually update the data:
        cfg_w.writelines(lines)
        print('Created file: ', fpath_cfg_test)

# endregion

print('\nSetup_darknet.py completed.\n')
for i in range(5, 0, -1):
    print('Starting training in', int(i), 'seconds.', end='\r')
    time.sleep(1)
print()
