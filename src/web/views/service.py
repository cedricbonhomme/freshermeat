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

from flask import Blueprint, request, render_template, flash, url_for, \
                  redirect, abort

from web.models import Service

service_bp = Blueprint('service_bp', __name__,
                       url_prefix='/service')


@service_bp.route('/<service_name>', methods=['GET'])
def service(service_name=None):
    #service_id = request.args.get('name')
    service = Service.query.filter(Service.name == service_name).first()
    if service is None:
        abort(404)
    if not service:
        flash('Unknown service.', 'warning')
        return redirect(url_for(services_bp.list_services))
    return render_template('service.html', service=service)
