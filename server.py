#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import time
import os.path
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, abort
from flask.ext.sqlalchemy import SQLAlchemy, event

from modules.configuration import Configuration

CONST_UPLOADER_PID_FILE = '/tmp/uploader.pid'

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


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    inserted_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    timestamp = db.Column(db.Integer)

    def __init__(self, name, timestamp, inserted_at=None):
        self.name = name

        if inserted_at is None:
            self.inserted_at = datetime.utcnow()
        self.timestamp = timestamp


@event.listens_for(File, 'after_update')
def update_actual_date(mapper, connection, target):
    target.updated_at = datetime.utcnow()


def get_file_object_or_create(file_name):
    file= File.query.filter_by(name=file_name).first()
    if file:
        return file
    else:
        return File(name=file_name, timestamp=None, inserted_at=None)



class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False)
    date = db.Column(db.DateTime)
    file_attrs = db.Column(db.String(128), unique=False)
    result_code = db.Column(db.Integer)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
    event_type = db.relationship('EventType', backref=db.backref('events', lazy='dynamic'))
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    file = db.relationship('File', backref=db.backref('files', lazy='dynamic'))

    def __init__(self, name, event_type, file, date, file_attrs, result_code):
        self.name = name

        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.event_type = event_type
        self.file = file
        self.file_attrs = file_attrs
        self.result_code = result_code

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
    files = File.query.all()
    events = Event.query.order_by('date desc').all()[:50]
    return render_template('index.html', message=message, files=files, events=events)


@app.route('/daemon/start')
def daemon_start():
    config = Configuration()
    config.load()
    cmd = [config.interpreter, os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploader.py')), 'start']
    subprocess.Popen(cmd)
    time.sleep(0.5)
    return redirect(url_for('daemon_status'))


@app.route('/daemon/stop')
def daemon_stop():
    config = Configuration()
    config.load()
    cmd = [config.interpreter, os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploader.py')), 'stop']
    subprocess.Popen(cmd)
    time.sleep(0.5)
    return redirect(url_for('daemon_status'))


@app.route('/daemon/restart')
def daemon_restart():
    config = Configuration()
    config.load()
    cmd = [config.interpreter, os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploader.py')), 'restart']
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


def init():
    db.create_all()
    db.session.add(EventType(u'Information'))
    db.session.add(EventType(u'Error'))
    db.session.add(EventType(u'File uploading'))
    db.session.add(EventType(u'File changed'))
    db.session.commit()


if __name__ == '__main__':
# TODO: Optparse maybe?
    if len(sys.argv) == 2:
        if 'init' == sys.argv[1]:
            init()
        else:
            print 'unknown command!'
            sys.exit(2)

    elif len(sys.argv) == 1:
        app.run()
    else:
        print('usage: %s [init]' % sys.argv[0])
        sys.exit(2)
