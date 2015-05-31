#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from datetime import datetime
import os
import os.path
import math
import json

import requests
from requests.auth import HTTPBasicAuth

from modules.daemon import Daemon
from modules.configuration import Configuration
from modules.utils import get_file_info, get_file_names
from modules.post import post_multipart

from server import (CONST_UPLOADER_PID_FILE, db, EventType, Event, get_file_object_or_create)



def file_log(filename, message):
    with open(filename, 'a') as f:
        f.write('%s %s\n' % (datetime.now().strftime('%Y %m %d %H:%M:%S'), message))


def upload_file(filename, file_object, current_file_timestamp):
    """
    server file uploader
    """
    base_name = os.path.basename(filename)
    file_attrs_str = str(get_file_info(filename))
    try:
        configuration = Configuration()
        configuration.load()
        api_key = configuration.api_key
        url = configuration.url
        payload = {'api_key': api_key, 'hide_old': 0}
        code, response = post_multipart(url=url, payload=payload,
                                        file_name=filename)

        print response
        event_type_uploading = EventType.query.get(3)
        event_post_results = Event(name='%s post results: %s' % (base_name, str({'code': code, 'response': response})),
                                   event_type=event_type_uploading, file=None, date=None, file_attrs=file_attrs_str,
                                   result_code=code)
        db.session.add(event_post_results)
        db.session.commit()
        if code == 200:
            task_id = (json.loads(response)).get('task_id')
            if task_id:
                ready = False
                t0 = time.time()# time started
                expected_waiting_time = 35
                loop_num = 0
                while not ready:
                    try:
                        r = requests.get(url, params={'task_id': task_id,
                                                      'api_key': api_key,
                                                      }, verify=False)
                        print r.text
                        if r.status_code == 200:
                            if json.loads(r.text).get('ready') is True:
                                # log ready
                                available = json.loads(r.text).get('available')
                                updated = json.loads(r.text).get('updated')
                                file_object.updated_at = datetime.utcnow()
                                file_object.timestamp = current_file_timestamp
                                db.session.add(file_object)
                                db.session.commit()

                                event_results = Event(name='%s upload successful!!! results: available: %d, updated %d' %
                                                           (base_name, available, updated),
                                                      event_type=event_type_uploading,
                                                      file=file_object,
                                                      date=None,
                                                      file_attrs=file_attrs_str,
                                                      result_code=r.status_code)
                                db.session.add(event_results)
                                db.session.commit()
                                break
                        else:
                            # reason?
                            reason = 'unknown'
                            event_results = Event(name='%s results: file not uploaded, reason %s' % (base_name, reason),
                                                      event_type=event_type_uploading,
                                                      file=None,
                                                      date = None,
                                                      file_attrs=file_attrs_str,
                                                      result_code= r.status_code)
                            db.session.add(event_results)
                            db.session.commit()
                            break

                    except Exception as e:
                        event_results = Event(name='%s: system error %s' % (base_name, e.args[0]),
                                                      event_type=event_type_uploading,
                                                      file=None,
                                                      date = None,
                                                      file_attrs=file_attrs_str,
                                                      result_code= None)
                        db.session.add(event_results)
                        db.session.commit()
                        break
                    time.sleep(expected_waiting_time)
                    current, total = 0, 0
                    try:
                        current = json.loads(r.text).get('state').get('current')
                        total = json.loads(r.text).get('state').get('total')
                    except:
                        pass
                    t = math.floor(time.time() - t0)
                    if total != 0 and current != 0 and loop_num != 0 :
                            expected_waiting_time = math.floor((total - current) * t / current)
                    loop_num += 1
    except ValueError as ve:
        event_type_error = EventType.query.get(2)
        event_configuration_error = Event(name='%d config error %s' % (base_name, ve.args[0]),
                                    event_type=event_type_error,file=None, date=None,
                                    file_attrs=file_attrs_str, result_code=None)
        db.session.add(event_configuration_error)
        db.session.commit()


class Uploader(Daemon):
    """
    Uploader - main working method
    """
    def run(self):
        configuration = Configuration()
        configuration.load()
        path = configuration.upload_folder
        tick = configuration.tick
        #file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fuckup.log'))
        while True:
            if path:
                for file_name in get_file_names(path):
                    file_changed = False
                    result = None
                    f = os.path.basename(file_name)
                    file_object = get_file_object_or_create(f)
                    current_file_info = get_file_info(file_name)
                    current_file_timestamp = current_file_info[0].replace('-', '').replace(':', '').replace(' ', '')
                    #file exist
                    if file_object.timestamp:
                        if file_object.timestamp < current_file_timestamp:
                            file_changed = True
                            upload_file(file_name, file_object, current_file_timestamp)
                    else:
                        file_changed = True
                        upload_file(file_name, file_object, current_file_timestamp)
            time.sleep(float(tick))

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
