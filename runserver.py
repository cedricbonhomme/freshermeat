#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2020 Cédric Bonhomme - https://www.cedricbonhomme.org
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

from freshermeat.bootstrap import application

with application.app_context():

    from freshermeat.web import views

    application.register_blueprint(views.admin_bp)
    application.register_blueprint(views.user_bp)
    application.register_blueprint(views.project_bp)
    application.register_blueprint(views.projects_bp)
    application.register_blueprint(views.organization_bp)
    application.register_blueprint(views.organizations_bp)
    application.register_blueprint(views.stats_bp)
    application.register_blueprint(views.submissions_bp)
    application.register_blueprint(views.submission_bp)

    # API v1
    application.register_blueprint(views.api.v1.blueprint_organization)
    application.register_blueprint(views.api.v1.blueprint_project)
    application.register_blueprint(views.api.v1.blueprint_code)
    application.register_blueprint(views.api.v1.blueprint_tag)
    application.register_blueprint(views.api.v1.blueprint_user)
    application.register_blueprint(views.api.v1.blueprint_release)
    application.register_blueprint(views.api.v1.blueprint_cve)
    application.register_blueprint(views.api.v1.blueprint_license)
    application.register_blueprint(views.api.v1.blueprint_language)
    application.register_blueprint(views.api.v1.blueprint_news)
    application.register_blueprint(views.api.v1.blueprint_feed)

    # API v2
    application.register_blueprint(views.api.v2.blueprint_project)


if __name__ == "__main__":
    application.run(host=application.config["HOST"], port=application.config["PORT"])
