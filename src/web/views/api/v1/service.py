#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bootstrap import application, manager

from web import models
from web.views.api.v1 import processors
from web.views.api.v1.common import url_prefix, auth_func

blueprint_service = manager.create_api_blueprint(models.Service,
                    url_prefix=url_prefix,
                    methods=['GET', 'POST', 'PUT', 'DELETE'],
                    preprocessors=dict(
                             #GET_SINGLE=[processors.auth_func],
                             #GET_MANY=[processors.auth_func],
                             POST=[processors.auth_func],
                             DELETE=[processors.auth_func]))
