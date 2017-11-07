#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bootstrap import application, manager

from web import models
from web.views.api.v1 import processors
from web.views.api.v1.common import url_prefix

blueprint_request = manager.create_api_blueprint(
    models.Request,
    url_prefix=url_prefix,
    methods=['POST'],
    preprocessors={
        'POST': [processors.post_preprocessor]
    },
    postprocessors={
        'POST': [processors.post_postprocessor]
    })
