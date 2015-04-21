#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib, urllib, urllib2, os


#test post
def generate_post():
    params = urllib.urlencode({'@number': 12345, '@type': 'issue', '@action': 'show'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 5000)
    conn.request("POST", '/test', params, headers)
    response = conn.getresponse()
    return response.status, response.reason


def generate_file_post():
    filename = 'testfile'
    url = 'http://localhost:5000/test'
    length = os.path.getsize(filename)
    file_data = open(filename, 'rb')
    pass
