#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2019  Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information : https://gitlab.com/cedric/Freshermeat
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
from flask_restless import ProcessingException

from bootstrap import db
from web.views.common import login_user_bundle
from web.models import User

logger = logging.getLogger(__name__)

def auth_func(*args, **kw):
    print('auth_func')
    if request.authorization:
        user = User.query.filter(User.login == request.authorization.username).first()
        if not user:
            raise ProcessingException("Couldn't authenticate your user",
                                      code=401)
        if not user.check_password(request.authorization.password):
            raise ProcessingException("Couldn't authenticate your user",
                                      code=401)
        if not user.is_active:
            raise ProcessingException("Couldn't authenticate your user", code=401)
        login_user_bundle(user)
    if not current_user.is_authenticated:
        raise ProcessingException(description='Not authenticated!', code=401)
