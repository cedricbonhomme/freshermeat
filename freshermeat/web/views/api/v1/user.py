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


from freshermeat.bootstrap import manager

from freshermeat.models import User
from freshermeat.web.views.api.v1 import processors
from freshermeat.web.views.api.v1.common import url_prefix


def pre_get_single(search_params=None, **kw):
    pass


def pre_get_many(search_params=None, **kw):
    filters = [
        dict(name="public_profile", op="eq", val=True),
    ]
    # Check if there are any filters there already.
    if "filters" not in search_params:
        search_params["filters"] = []
    search_params["filters"].extend(filters)


blueprint_user = manager.create_api_blueprint(
    User,
    url_prefix=url_prefix,
    include_columns=["login"],
    methods=["GET"],
    preprocessors={"GET_MANY": [pre_get_many]},
)
