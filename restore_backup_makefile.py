#!/usr/bin/env python3
"""Checks if the makefile_BACKUP exists and uses it as the makefile."""
import os

fpath_source = os.path.realpath(__file__).rpartition('/')[0] + '/'
if os.path.isfile(fpath_source + 'darknet/Makefile_BACKUP'):
    os.unlink(fpath_source + 'darknet/Makefile')
    os.rename(fpath_source + 'darknet/Makefile_BACKUP', fpath_source + 'darknet/Makefile')
else:
    print('No Makefile backup found. Backup will created later: Makefile_BACKUP')
