#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import time
import os.path
from datetime import datetime
import ConfigParser

from flask import Flask, render_template, request, redirect, url_for, abort
from flask.ext.sqlalchemy import SQLAlchemy

from uploader import CONST_UPLOADER_PID_FILE

app = Flask(__name__)
app.config.from_pyfile('server.cfg')
db = SQLAlchemy(app)


def get_or_abort(model, object_id, code=404):
    result = model.query.get(object_id)
    return result or abort(code)


class EventType(db.Model):
    __tablename__ = 'event_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Event type %d (%s)>' % (self.id, self.name)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False)
    date = db.Column(db.DateTime)
    file_size = db.Column(db.String(32), unique=False)
    file_attrs = db.Column(db.String(128), unique=False)
    file_timestamp = db.Column(db.String(32), unique=False)
    operation_code = db.Column(db.Integer)

    def __init__(self, name, date, file_size, file_attrs, file_timestamp, operation_code):
        self.name = name

        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.file_size = file_size
        self.file_attrs = file_attrs
        self.file_timestamp = file_timestamp
        self.operation_code = operation_code

    def __repr__(self):
        return '<Event #%d (%s)>' % (self.id, self.date.strftime('%Y %m %d %H:%M:%S'))


@app.route('/')
def index():
    return redirect(url_for('daemon_status'))


@app.route('/daemon/status')
def daemon_status():
    if os.path.isfile(CONST_UPLOADER_PID_FILE):
        pf = open(CONST_UPLOADER_PID_FILE, 'r')
        pid = pf.read().strip()
        message = 'Daemon is running. PID is %s' % pid
    else:
        message = 'Daemon is not running...'
    return render_template('index.html', message=message)


@app.route('/daemon/start')
def daemon_start():
    cmd = ['/usr/bin/env', 'python', os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploader.py')), 'start']
    subprocess.Popen(cmd)
    time.sleep(0.5)
    return redirect(url_for('daemon_status'))


@app.route('/daemon/stop')
def daemon_stop():
    cmd = ['/usr/bin/env', 'python', os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploader.py')), 'stop']
    subprocess.Popen(cmd)
    time.sleep(0.5)
    return redirect(url_for('daemon_status'))


@app.route('/daemon/restart')
def daemon_restart():
    cmd = ['/usr/bin/env', 'python', os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploader.py')), 'restart']
    subprocess.Popen(cmd)
    time.sleep(0.5)
    return redirect(url_for('daemon_status'))


@app.route('/test', methods=['POST'])
def test_post():
    if request.files.get('file'):
        file_name = request.files['file'].filename
        blob = request.files['file'].read()
        size = len(blob)
        print ('file in POST: %s, size: %d ' % (file_name, size))
    print ('path: %s, number: %s' % (request.path, request.form.get('@number')))
    return 'OK'


if __name__ == '__main__':
    app.run()
