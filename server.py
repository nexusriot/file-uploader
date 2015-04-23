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
