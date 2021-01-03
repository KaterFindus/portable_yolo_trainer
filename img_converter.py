#!/usr/bin/env python3
import os
import cv2
import time
import logging
import concurrent.futures

t0 = time.perf_counter()


def convert(file_in, output_dir, ext_out):
    # get name
    name = file_in.rpartition('/')[2].rpartition('.')[0]
    image = cv2.imread(file_in)
    cv2.imwrite(str(output_dir + name + ext_out), image)
    print('Processed: ' + name)


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]\t%(message)s')
logging.disable()

fpath_in = input('Provide input path:\n >> ')
if len(fpath_in) == 0:
    fpath_in = '/home/findux/Desktop/TEST_IN/'
    logging.info('[DEFAULT]   Using ' + fpath_in)
if not fpath_in.endswith('/'): fpath_in = fpath_in + '/'
logging.info('Path IN: ' + fpath_in)

fpath_out = '/home/findux/Desktop/TEST_OUT/'
logging.info('Path OUT: ' + fpath_out)

target_ext = '.jpg'
logging.info('Target extension: ' + target_ext)

input_file_list = sorted(os.listdir(fpath_in))
input_file_list = [fpath_in + file for file in input_file_list]

paths_out = [fpath_out for i in range(len(input_file_list))]
extensions_dest = [target_ext for i in range(len(input_file_list))]

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(convert, input_file_list, paths_out, extensions_dest)
t1 = time.perf_counter()
print('Done in {} seconds.'.format(t1-t0))

# # Old, manual way:
# t0 = time.perf_counter()
# fpath_dataset = '/home/findux/Desktop/TEST_IN/'
# fpath_output = '/home/findux/Desktop/TEST_OUT/'
# ext_src = 'tif'
# ext_dest = 'jpg'
# files = sorted(os.listdir(fpath_dataset))
# files = [fpath_dataset + file for file in files if file.endswith(ext_src)]
# for file in files:
#     name = file.rpartition('/')[2].rpartition('.')[0]
#     cv2.imwrite(fpath_output + name + ext_dest, cv2.imread(file))
#     print('Processed {}.'.format(name))
# t1 = time.perf_counter()
# print('Done in {} seconds.'.format(t1-t0))