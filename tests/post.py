#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib, urllib, urllib2, os

# TODO: Is poster really needed?
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


def post():
    params = urllib.urlencode({'@number': 12345, '@type': 'issue', '@action': 'show'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 5000)
    conn.request("POST", '/test', params, headers)
    response = conn.getresponse()
    return response.status, response.reason


def post_multipart():
    register_openers()
    filename = 'testfile'
    url = 'http://localhost:5000/test'
    values = {'form': open(filename), 'desc': 'description'}
    data, headers = multipart_encode(values)
    headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    request = urllib2.Request(url, data, headers)
    request.unverifiable = True
    response = urllib2.urlopen(request)
    page = response.read()


def main():
    post_multipart()


if __name__ == '__main__':
    main()
