#!/usr/bin/env python3

import os
import shutil

fpath_source = os.path.realpath(__file__).rpartition('/')[0] + '/'
os.chdir(fpath_source)
fpath_dset = fpath_source + 'training_set/'

# Get files
files = sorted(os.listdir(fpath_dset))
# files = [fpath_dset + file for file in files]

empties_txt = []
for file in files:
    if os.path.getsize('training_set/' + file) < 2:
        empties_txt.append(file)
print(str(len(empties_txt)) + ' empty files found.')

empties_tif = [file[:-4] + '.tif' for file in empties_txt]
assert len(empties_txt) == len(empties_tif)

empties_both = empties_tif + empties_txt
assert len(empties_both) == len(empties_tif) * 2

# large = [file for file in files if file not in empties_both]
# [print(file, os.path.getsize(fpath_dset + file)) for file in large]


os.mkdir(fpath_dset + 'empties')
for file in empties_both:
    shutil.move(fpath_dset + file, fpath_dset + 'empties/' + file)