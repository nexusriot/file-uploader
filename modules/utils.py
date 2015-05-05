#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import stat
import time
from os import listdir
from os.path import isfile, isdir, join


def get_file_info(file_name):
    file_format = "%Y-%m-%d %H:%M:%S"
    stats = os.stat(file_name)
    modification_time = time.strftime(file_format, time.localtime(stats[stat.ST_MTIME]))
    access_time = time.strftime(file_format, time.localtime(stats[stat.ST_ATIME]))
    return modification_time, access_time


def get_file_names(path):
    if isdir(path):
        return [os.path.join(path, f) for f in listdir(path) if isfile(join(path, f))]
    return []




