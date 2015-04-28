#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests


def post_regular(url='http://localhost:5000/test', payload={'@number': 12345}):
    code = 0
    try:
        r = requests.post(url, data=payload)
        code = r.status_code
    except requests.exceptions.ConnectionError as e:
        code = e.args[0].reason.errno
    return code


def post_multipart(url='http://localhost:5000/test', payload={'@number': 1},
                   file_name=os.path.abspath(os.path.join(os.path.dirname(__file__), 'testfile'))):
    code = 0
    try:
        files = {'file': open(file_name, 'rb')}
        try:
            pass
            r = requests.post(url, files=files, data=payload)
            code = r.status_code
        except requests.exceptions.ConnectionError as e:
            code = e.args[0].reason.errno
    except IOError:
        code = -1
    return code


def main():
    print (post_regular())
    print (post_multipart())


if __name__ == '__main__':
    main()
