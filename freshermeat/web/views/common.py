#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2020 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information: https://git.sr.ht/~cedric/freshermeat
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

from flask import current_app
from flask_login import login_user
from flask_principal import (Identity, Permission, RoleNeed,
                                 session_identity_loader, identity_changed)

admin_role = RoleNeed('admin')
api_role = RoleNeed('api')

admin_permission = Permission(admin_role)
api_permission = Permission(api_role)


def login_user_bundle(user):
    login_user(user)
    identity_changed.send(current_app, identity=Identity(user.id))
    session_identity_loader()
    # TODO: set last_seen
