#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bootstrap import manager

from web import models
from web.views.api.v1 import processors
from web.views.api.v1.common import url_prefix


blueprint_tag = manager.create_api_blueprint(
    models.Tag,
    url_prefix=url_prefix,
    methods=['GET'])
