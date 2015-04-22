#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import os
import requests


def post():
    payload = {'@number': 12345}
    r = requests.post('http://localhost:5000/test', data=payload)
    return r.status_code


def post_multipart():
    payload = {'@number': 1}
    url = 'http://localhost:5000/test'
    files = {'file': open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'testfile')), 'rb')}
    r = requests.post(url, files=files, data=payload)
    return r.status_code


def main():
    post()
    post_multipart()


if __name__ == '__main__':
    main()
