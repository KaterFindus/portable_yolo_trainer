#!/usr/bin/env python3
import time
import datetime
import os

# now = time.localtime()
# nowd = datetime.datetime.now()
# print(time.strftime('%Y-%M-%d_%H-%m', now))
# print(nowd)

# a = {'fuck': 1,
#      'the': 2,
#      'duck': 3}
# for param, val in a.items():
#     print(param, val)
# longest = 0
# [longest := len(param) if len(param) > longest else longest for param in list(a.keys())]
# print(longest)

# s = 'DEBUG=0'
# print(s.split('='))

# l = ('ab-cd', 'bcde', 'efgh')
# l = [line.partition('-')[0] if line.startswith('a') else line for line in l]
# print(l)

# change = [(0, 2),
#           (1, 0),
#           (2, 1)]

fpath = '/media/findux/DATA/Code/Litter_detector/Data/BACKUP_001-730/'
files = os.scandir(fpath)
files_walked = os.walk(fpath)

print(files_walked)
print(files_walked)







