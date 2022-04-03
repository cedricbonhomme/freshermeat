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

import logging
import asyncio
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import and_

from freshermeat.bootstrap import application, db
import freshermeat.models
import freshermeat.scripts
from freshermeat.workers import fetch_cve, fetch_release, fetch_project_news


logger = logging.getLogger("manager")

Migrate(application, db)
manager = Manager(application)
manager.add_command("db", MigrateCommand)


@manager.command
def uml_graph():
    "UML graph from the models."
    with application.app_context():
        freshermeat.models.uml_graph(db)


@manager.command
def db_empty():
    "Will drop every datas stocked in db."
    with application.app_context():
        freshermeat.models.db_empty(db)


@manager.command
def db_create():
    "Will create the database."
    with application.app_context():
        freshermeat.models.db_create(
            db,
            application.config["DB_CONFIG_DICT"],
            application.config["DATABASE_NAME"],
        )


@manager.command
def db_init():
    "Will create the database from conf parameters."
    with application.app_context():
        freshermeat.models.db_init(db)


@manager.command
def create_user(login, password):
    "Initializes a user"
    print("Creation of the user {} ...".format(login))
    with application.app_context():
        freshermeat.scripts.create_user(login, password, False)


@manager.command
def create_admin(login, password):
    "Initializes an admin user"
    print("Creation of the admin user {} ...".format(login))
    with application.app_context():
        freshermeat.scripts.create_user(login, password, True)


@manager.command
def import_languages(json_file):
    "Import languages from a JSON file"
    print("Importing languages from {} ...".format(json_file))
    with application.app_context():
        freshermeat.scripts.import_languages(json_file)


@manager.command
def import_starred_projects_from_github(user):
    "Import GitHub starred projects of a user."
    print("Importing GitHub starred projects of {} ...".format(user))
    with application.app_context():
        freshermeat.scripts.import_starred_projects_from_github(user)


@manager.command
def import_project_from_github(owner, repo, submitter_id):
    "Import a project from GitHub."
    with application.app_context():
        stdout = freshermeat.scripts.import_project_from_github(
            owner, repo, submitter_id
        )
        print(stdout)


@manager.command
def import_project_from_gitlab(repository, submitter_id):
    "Import a project from GitLab."
    with application.app_context():
        stdout = freshermeat.scripts.import_project_from_gitlab(
            repository, submitter_id
        )
        print(stdout)


@manager.command
def import_osi_approved_licenses():
    "Import OSI approved licenses."
    print("Importing OSI approved licenses...")
    with application.app_context():
        freshermeat.scripts.import_osi_approved_licenses()


@manager.command
def fetch_cves(cve_vendor=None):
    "Crawl the CVE."
    with application.app_context():

        query = freshermeat.models.Project.query.filter(
            and_(
                freshermeat.models.Project.cve_vendor != "",
                freshermeat.models.Project.cve_product != "",
            )
        )
        if cve_vendor:
            query = query.filter(freshermeat.models.Project.cve_vendor == cve_vendor)
        projects = query.all()

        logger.info("Starting CVE fetcher.")

        start = datetime.now()
        loop = asyncio.get_event_loop()
        fetch_cve.retrieve(loop, projects)
        loop.close()
        end = datetime.now()

        logger.info("CVE fetcher finished in {} seconds.".format((end - start).seconds))


@manager.command
def fetch_releases():
    """Automatic release tracking
    Retrieves the new releases of the projects."""
    github_releases = freshermeat.models.Project.query.filter(
        freshermeat.models.Project.automatic_release_tracking.like("github:%")
    )
    gitlab_releases = freshermeat.models.Project.query.filter(
        freshermeat.models.Project.automatic_release_tracking.like("gitlab:%")
    )
    # changelog_releases = freshermeat.models.Project.query.filter(
    # freshermeat.models.Project.automatic_release_tracking.like('changelog:%'))

    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(maxsize=10)

    producer_coro_github = fetch_release.retrieve_github(queue, github_releases)
    producer_coro_gitlab = fetch_release.retrieve_gitlab(queue, gitlab_releases)
    # producer_coro_changelog = fetch_release.retrieve_changelog(queue,
    # changelog_releases)
    consumer_coro = fetch_release.insert_releases(queue, 2)

    loop.run_until_complete(
        asyncio.gather(
            producer_coro_github,
            producer_coro_gitlab,
            # producer_coro_changelog,
            consumer_coro,
        )
    )
    loop.close()


@manager.command
def fetch_news():
    """Automatic news tracking
    Retrieves the new of the projects."""
    feeds = freshermeat.models.Feed.query.all()

    fetch_project_news.retrieve(feeds)


if __name__ == "__main__":
    manager.run()
