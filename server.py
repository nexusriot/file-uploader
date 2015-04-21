#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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
    return 'Index'

@app.route('/daemon/status')
def daemon_status():
    if os.path.isfile(CONST_UPLOADER_PID_FILE):
        pf = open(CONST_UPLOADER_PID_FILE, 'r')
        pid = pf.read().strip()
        return 'Daemon is running. PID is %s' % (pid)
    else:
        return 'Daemon is not running...'


@app.route('/daemon/start')
def daemon_start_command():
    return redirect(url_for('daemon_status'))


if __name__ == '__main__':
    app.run()
