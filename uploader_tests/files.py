#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from datetime import datetime

from server import db, File, get_file_object_or_create
from modules.configuration import Configuration
from modules.utils import get_file_info, get_file_names


def main():
    configutation = Configuration().load()
    path = configutation.get('upload_folder')
    if path:
        for file_name in get_file_names(path):
            f = os.path.basename(file_name)
            file_object = get_file_object_or_create(f)
            current_file_info = get_file_info(file_name)
            current_file_timestamp = current_file_info[0].replace('-', '').replace(':', '').replace(' ', '')
            # file exist
            if file_object.timestamp:
                if file_object.timestamp < current_file_timestamp:
                    # 1. TODO Do POST
                    # 2. Update model
                    file_object.updated_at = datetime.utcnow()
                    file_object.timestamp = current_file_timestamp
            else:
                # 1. TODO: Do POST
                file_object.updated_at = datetime.utcnow()
                file_object.timestamp = current_file_timestamp
            db.session.add(file_object)
            db.session.commit()


if __name__ == '__main__':
    main()
