#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from server import db, EventType, Event, File
from modules.utils import get_file_names
import time, datetime


def main():

    f1 = File(name='Koko', timestamp='201505062222')
    db.session.add(f1)
    db.session.commit()


    f1l = File.query.get(1)
    f1l.name = '222'
    db.session.add(f1l)
    db.session.commit()


if __name__ == '__main__':
    main()




