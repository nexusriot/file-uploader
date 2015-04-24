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
                matches=[x for x in ['server', 'upload', 'python'] if x in cfg.sections()]
                for match in matches:
                    if match == 'server':
                        try:
                            server_address = cfg.get(match, 'address')
                            self.address = server_address
                        except ConfigParser.NoOptionError:
                            print('Required server option address is missing!')
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

        if None in [self.address, self.url, self.interpreter, self.api_key]:
            raise ValueError('Invalid configuration file! Please check example.')

    def save(self):
        pass


def main():
    configuration = Configuration()
    configuration.load()
    print "url: %s, api_key: %s" % (configuration.url, configuration.api_key)


if __name__ == '__main__':
    main()