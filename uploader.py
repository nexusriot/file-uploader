#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import os.path
from modules.daemon import Daemon
from tests.post import post_regular, post_multipart


CONST_UPLOADER_PID_FILE = '/tmp/uploader.pid'


class Uploader(Daemon):
    def run(self):

        #file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fuck.dat'))
        while True:
            status_code = post_multipart()
            status_code = post_regular()
            #with open(file_name, 'a') as f:
            #    f.write('%s;' % (str(status_code)))
            time.sleep(2)

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
