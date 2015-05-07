#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from datetime import datetime

from server import db, File, EventType, Event, get_file_object_or_create
from modules.configuration import Configuration
from modules.utils import get_file_info, get_file_names


def main():
    configutation = Configuration().load()
    path = configutation.get('upload_folder')
    if path:
        for file_name in get_file_names(path):
            file_changed = False
            result = None
            f = os.path.basename(file_name)
            file_object = get_file_object_or_create(f)
            current_file_info = get_file_info(file_name)
            current_file_timestamp = current_file_info[0].replace('-', '').replace(':', '').replace(' ', '')
            # file exist
            if file_object.timestamp:
                if file_object.timestamp < current_file_timestamp:
                    file_changed = True
                    # 2. TODO: Do POST, set result
                    result = 200
                    # 2. Update model
                    file_object.updated_at = datetime.utcnow()
                    file_object.timestamp = current_file_timestamp
            else:
                # 1. TODO: Do POST, set result
                result = 200
                file_object.updated_at = datetime.utcnow()
                file_object.timestamp = current_file_timestamp
                file_changed = True
            db.session.add(file_object)
            db.session.commit()

            if file_changed:
                event_type_file_changed = EventType.query.get(4)
                event_file_changed = Event(name='%s changed ' % f, event_type=event_type_file_changed,
                                               file=file_object, date=None, file_attrs=str(current_file_info),
                                               result_code=None)
                db.session.add(event_file_changed)
                db.session.commit()

            if result:
                event_type_uploading = EventType.query.get(3)
                event_file_uploading = Event(name='%s uploading ' % f, event_type=event_type_uploading,
                                             file=file_object, date=None, file_attrs=str(current_file_info),
                                             result_code=result)
                db.session.add(event_file_uploading)
                db.session.commit()


if __name__ == '__main__':
    main()
