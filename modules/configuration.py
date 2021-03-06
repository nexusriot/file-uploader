#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ConfigParser
import re
import os
import os.path


# Configuration singleton
class Configuration(object):
    _instance = None

    address = None
    url = None
    interpreter = None
    api_key = None
    upload_folder = None
    tick = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def load(self):
        file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'daemon.cfg'))

        if os.path.isfile(file_name):
            cfg = ConfigParser.ConfigParser()
            try:
                cfg.read(file_name)
                matches = [x for x in ['server', 'upload', 'python'] if x in cfg.sections()]
                for match in matches:
                    if match == 'server':
                        try:
                            server_address = cfg.get(match, 'address')
                            self.address = server_address
                        except ConfigParser.NoOptionError:
                            print('Required server option address is missing!')
                        try:
                            upload_folder = cfg.get(match, 'upload_folder')
                            self.upload_folder = upload_folder
                        except ConfigParser.NoOptionError:
                            print('Required server option upload_folder is missing!')
                        try:
                            tick = cfg.get(match, 'tick')
                            self.tick = tick
                        except ConfigParser.NoOptionError:
                            print('Required server option tick is missing!')
                    elif match == 'upload':
                        try:
                            upload_url = cfg.get(match, 'url')
                            url_template = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                                            '(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                            if re.match(url_template, upload_url):
                                self.url = upload_url
                            else:
                                raise ValueError('Invalid url')

                        except ConfigParser.NoOptionError:
                            print('Required upload option url is missing!')
                        except ValueError:
                            print ('Invalid url, please configure correct one!')
                        try:
                            api_key = cfg.get(match, 'api_key')
                            self.api_key = api_key
                        except ConfigParser.NoOptionError:
                            print ("Required option api_key is missing!")

                    elif match == 'python':
                        try:
                            interpreter = cfg.get(match, 'interpreter')
                            self.interpreter = interpreter
                        except ConfigParser.NoOptionError:
                            print('Interpreter name required!')
            except ConfigParser.ParsingError:
                print('Invalid config file!')

        if None in [self.address, self.url, self.interpreter, self.api_key, self.upload_folder]:
            raise ValueError('Invalid configuration file! Please check example.')

        return {'address': self.address, 'url': self.url, 'interpreter': self.interpreter,
                'api_key': self.api_key, 'upload_folder': self.upload_folder, 'tick': self.tick}

    def save(self):
        raise NotImplementedError


def main():
    configuration = Configuration()
    print (configuration.load())
    try:
        configuration.save()
    except NotImplementedError, e:
        print("NotImplementedError catched ")


if __name__ == '__main__':
    main()