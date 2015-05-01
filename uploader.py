#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import os.path
from modules.daemon import Daemon
from modules.configuration import Configuration

from uploader_tests.post import post, post_multipart
from server import (CONST_UPLOADER_PID_FILE, db, EventType, Event)


def file_log(filename, message):
    with open(filename, 'a') as f:
        f.write('%s %s\n' % (datetime.datetime.now().strftime('%Y %m %d %H:%M:%S'), message))


class Uploader(Daemon):
    def run(self):
        file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fuckup.log'))
        while True:
            ### step1: get configuration
            config = Configuration().load()
            ### step2: then check the file for post
            # TODO: get last from log?
            # if date of local file < remote, post the file




            #status_code = post_multipart()
            #status_code = post()
            time.sleep(20)

    def stop(self):
        Daemon.stop(self)


if __name__ == '__main__':
    daemon = Uploader(CONST_UPLOADER_PID_FILE)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print 'Unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
