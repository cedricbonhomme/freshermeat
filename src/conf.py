#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Program variables.

This file contain the variables used by the application.
"""
import os
import logging
from urllib.parse import urlsplit

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.abspath(".")
API_ROOT = '/api/v1.0'


ON_HEROKU = int(os.environ.get('HEROKU', 0)) == 1
DEFAULTS = {"platform_url": "https://services.securitymadein.lu/",
            "admin_email": "info@smile.lu",
            "token_validity_period": "3600",
            "default_max_error": "3",
            "log_path": "services.log",
            "log_level": "info",
            "secret_key": "",
            "security_password_salt": "",
            "enabled": "false",
            "notification_email": "info@smile.lu",
            "tls": "false",
            "ssl": "true",
            "host": "0.0.0.0",
            "port": "5000"
            }

if not ON_HEROKU:
    import configparser as confparser
    # load the configuration
    config = confparser.SafeConfigParser(defaults=DEFAULTS)
    config.read(os.path.join(BASE_DIR, "instance/conf.cfg"))
else:
    class Config(object):
        def get(self, _, name):
            return os.environ.get(name.upper(), DEFAULTS.get(name))

        def getint(self, _, name):
            return int(self.get(_, name))

        def getboolean(self, _, name):
            value = self.get(_, name)
            if value == 'true':
                return True
            elif value == 'false':
                return False
            return None
    config = Config()


try:
    PLATFORM_URL = config.get('misc', 'platform_url')
except:
    PLATFORM_URL = "https://services.securitymadein.lu/"
ADMIN_EMAIL = config.get('misc', 'admin_email')
SECURITY_PASSWORD_SALT = config.get('misc', 'security_password_salt')
try:
    TOKEN_VALIDITY_PERIOD = config.getint('misc', 'token_validity_period')
except:
    TOKEN_VALIDITY_PERIOD = int(config.get('misc', 'token_validity_period'))
if not ON_HEROKU:
    LOG_PATH = os.path.abspath(config.get('misc', 'log_path'))
else:
    LOG_PATH = ''
LOG_LEVEL = {'debug': logging.DEBUG,
             'info': logging.INFO,
             'warn': logging.WARN,
             'error': logging.ERROR,
             'fatal': logging.FATAL}[config.get('misc', 'log_level')]

NOTIFICATION_EMAIL = config.get('notification', 'notification_email')
NOTIFICATION_HOST = config.get('notification', 'host')
NOTIFICATION_PORT = config.getint('notification', 'port')
NOTIFICATION_TLS = config.getboolean('notification', 'tls')
NOTIFICATION_SSL = config.getboolean('notification', 'ssl')
NOTIFICATION_USERNAME = config.get('notification', 'username')
NOTIFICATION_PASSWORD = config.get('notification', 'password')

CSRF_ENABLED = True
# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5
