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
API_v1_ROOT = '/api/v1.0'


ON_HEROKU = int(os.environ.get('HEROKU', 0)) == 1

# LOG_LEVEL = {'debug': logging.DEBUG,
#              'info': logging.INFO,
#              'warn': logging.WARN,
#              'error': logging.ERROR,
#              'fatal': logging.FATAL}[config.get('misc', 'log_level')]
