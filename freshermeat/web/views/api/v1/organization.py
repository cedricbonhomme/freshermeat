#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2022 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information: https://sr.ht/~cedric/freshermeat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from freshermeat.bootstrap import application, manager

from freshermeat.models import Organization
from freshermeat.web.views.api.v1 import processors
from freshermeat.web.views.api.v1.common import url_prefix


def pre_get_many(search_params=None, **kw):
    order_by = [{"field": "last_updated", "direction": "desc"}]
    if "order_by" not in search_params:
        search_params["order_by"] = []
    search_params["order_by"].extend(order_by)


blueprint_organization = manager.create_api_blueprint(
    Organization,
    url_prefix=url_prefix,
    methods=["GET", "POST", "PUT", "DELETE"],
    preprocessors=dict(
        GET_MANY=[pre_get_many],
        POST=[processors.auth_func],
        PUT=[processors.auth_func],
        DELETE=[processors.auth_func],
        DELETE_SINGLE=[processors.auth_func],
    ),
)
