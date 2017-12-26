#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bootstrap import manager

from web import models
from web.views.api.v1 import processors
from web.views.api.v1.common import url_prefix

def pre_get_single(search_params=None, **kw):
    pass


def pre_get_many(search_params=None, **kw):
    filters = [dict(name='public_profile', op='eq', val=True),
               dict(name='is_api', op='eq', val=False)]
    # Check if there are any filters there already.
    if 'filters' not in search_params:
        search_params['filters'] = []
    search_params['filters'].extend(filters)


blueprint_user = manager.create_api_blueprint(
        models.User,
        url_prefix=url_prefix,
        include_columns=['nickname'],
        methods=['GET'],
        preprocessors={
            'GET_MANY': [pre_get_many]
        }
    )
