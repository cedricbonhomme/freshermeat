#! /usr/bin/env python
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
from freshermeat import commands
from freshermeat.bootstrap import application


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.uml_graph)
    app.cli.add_command(commands.db_empty)
    app.cli.add_command(commands.db_create)
    app.cli.add_command(commands.db_init)
    app.cli.add_command(commands.create_user)
    app.cli.add_command(commands.create_admin)
    app.cli.add_command(commands.import_languages)
    app.cli.add_command(commands.import_starred_projects_from_github)
    app.cli.add_command(commands.import_project_from_github)
    app.cli.add_command(commands.import_project_from_gitlab)
    app.cli.add_command(commands.import_osi_approved_licenses)
    app.cli.add_command(commands.fetch_cves)
    app.cli.add_command(commands.fetch_releases)
    app.cli.add_command(commands.fetch_news)


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

    # API v2
    application.register_blueprint(views.api.v2.api_blueprint)

    register_commands(application)


if __name__ == "__main__":
    application.run(host=application.config["HOST"], port=application.config["PORT"])
