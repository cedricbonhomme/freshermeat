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

from freshermeat.models import Code
from freshermeat.web.views.api.v1 import processors
from freshermeat.web.views.api.v1.common import url_prefix


blueprint_code = manager.create_api_blueprint(
    Code,
    url_prefix=url_prefix,
    methods=["GET", "DELETE", "DELETE_SINGLE"],
    preprocessors=dict(
        DELETE_SINGLE=[processors.auth_func], DELETE=[processors.auth_func]
    ),
)
