#! /usr/bin/env python
# -*- coding: utf-8 -

# required imports and code exection for basic functionning

import os
import logging

import conf

def set_logging(log_path=None, log_level=logging.INFO, modules=(),
                log_format='%(asctime)s %(levelname)s %(message)s'):
    if not modules:
        modules = ('root', 'bootstrap', 'runserver', 'web',)
    if conf.ON_HEROKU:
        log_format = '%(levelname)s %(message)s'
    if log_path:
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        if not os.path.exists(log_path):
            open(log_path, 'w').close()
        handler = logging.FileHandler(log_path)
    else:
        handler = logging.StreamHandler()
    formater = logging.Formatter(log_format)
    handler.setFormatter(formater)
    for logger_name in modules:
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)
        for handler in logger.handlers:
            handler.setLevel(log_level)
        logger.setLevel(log_level)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create Flask application
application = Flask('web', instance_relative_config=True)
application.config.from_pyfile(os.environ.get('APPLICATION_SETTINGS',
                                            'development.cfg'),
                                silent=False)

# set_logging(application.config['LOG_PATH'],
#             log_level=application.config['LOG_LEVEL'])

db = SQLAlchemy(application)

# Create the Flask-Restless API manager.
import flask_restless
manager = flask_restless.APIManager(application, flask_sqlalchemy_db=db)


def populate_g():
    from flask import g
    g.db = db
    g.app = application
