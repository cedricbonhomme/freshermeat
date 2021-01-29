#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2021 Cédric Bonhomme - https://www.cedricbonhomme.org
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

import logging
from flask import request
from flask_login import current_user
from flask_restx import abort

from freshermeat.web.views.common import login_user_bundle
from freshermeat.models import User

logger = logging.getLogger(__name__)


def auth_func(func):
    def wrapper(*args, **kwargs):
        user = None

        if request.authorization:
            user = User.query.filter(
                User.login == request.authorization.username
            ).first()
            if not user.check_password(request.authorization.password):
                abort(401, Error="Couldn't authenticate your user.")
        elif "X-API-KEY" in request.headers:
            token = request.headers.get("X-API-KEY", False)
            if token:
                user = User.query.filter(User.apikey == token).first()

        if not user:
            abort(401, Error="Couldn't authenticate your user.")
        if not user.is_active:
            abort(401, Error="Couldn't authenticate your user.")

        login_user_bundle(user)

        if not current_user.is_authenticated:
            abort(401, Error="Couldn't authenticate your user.")

        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper
