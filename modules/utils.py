#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import stat
import time


def get_file_info(file_name):
    file_format = "%Y %m %d %H:%M:%S"
    stats = os.stat(file_name)
    modification_time = time.strftime(file_format, time.localtime(stats[stat.ST_MTIME]))
    access_time = time.strftime(file_format, time.localtime(stats[stat.ST_ATIME]))
    return modification_time, access_time
