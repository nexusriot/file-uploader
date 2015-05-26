import requests
import os, os.path


def post(url, payload):
    try:
        r = requests.post(url, data=payload)
        code = r.status_code
    except requests.exceptions.ConnectionError as e:
        code = e.args[0].reason.errno
    return code


def post_multipart(url, payload, file_name):
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