import requests
import os, os.path
from requests.auth import HTTPBasicAuth


def post(url, payload):
    try:
        r = requests.post(url, data=payload)
        code = r.status_code
    except requests.exceptions.ConnectionError as e:
        code = e.args[0].reason.errno
    return code


def post_multipart(url, payload, file_name):
    response = None
    try:
        files = {'upload': open(file_name, 'rb')}
        try:
            r = requests.post(url, files=files, data=payload, verify=False)
            code = r.status_code
            response = r.text
        except requests.exceptions.ConnectionError as e:
            code = e.args[0].reason.errno
            response = 'connection error'
    except IOError:
        code = -1
        response = 'I/O error'

    return code, response