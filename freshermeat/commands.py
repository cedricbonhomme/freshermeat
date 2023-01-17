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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# You should have received a copy of the GNU Affero General Public License
import asyncio
import logging
from datetime import datetime

import click
from sqlalchemy import and_

import freshermeat.models
import freshermeat.scripts
from freshermeat.bootstrap import application
from freshermeat.bootstrap import db
from freshermeat.workers import fetch_cve
from freshermeat.workers import fetch_project_news
from freshermeat.workers import fetch_release


logger = logging.getLogger("manager")


@application.cli.command("uml_graph")
def uml_graph():
    "UML graph from the models."
    freshermeat.models.uml_graph(db)


@application.cli.command("db_empty")
def db_empty():
    "Will drop every datas stocked in db."
    freshermeat.models.db_empty(db)


@application.cli.command("db_create")
def db_create():
    "Will create the database."
    freshermeat.models.db_create(
        db,
        application.config["DB_CONFIG_DICT"],
        application.config["DATABASE_NAME"],
    )


@application.cli.command("db_init")
def db_init():
    "Will create the database from conf parameters."
    freshermeat.models.db_init(db)


@application.cli.command("create_user")
@click.option("--login", default="admin", help="Login")
@click.option("--password", default="password", help="Password")
def create_user(login, password):
    "Initializes a user"
    print(f"Creation of the user {login} ...")
    freshermeat.scripts.create_user(login, password, False)


@application.cli.command("create_admin")
@click.option("--login", default="admin", help="Login")
@click.option("--password", default="password", help="Password")
def create_admin(login, password):
    "Initializes an admin user"
    print(f"Creation of the admin user {login} ...")
    freshermeat.scripts.create_user(login, password, True)


@application.cli.command("import_languages")
@click.option(
    "--json_file",
    default="var/languages.json",
    help="Import languages from a JSON file.",
)
def import_languages(json_file):
    "Import languages from a JSON file"
    print(f"Importing languages from {json_file} ...")
    freshermeat.scripts.import_languages(json_file)


@application.cli.command("import_starred_projects_from_github")
@click.option("--user", help="Import starred projects of a user from GitHub.")
def import_starred_projects_from_github(user):
    "Import GitHub starred projects of a user."
    print(f"Importing GitHub starred projects of {user} ...")
    freshermeat.scripts.import_starred_projects_from_github(user)


@application.cli.command("import_project_from_github")
@click.option("--owner", help="Owner")
@click.option("--repo", help="Repository")
@click.option("--submitter_id", help="Id of the submitter")
def import_project_from_github(owner, repo, submitter_id):
    "Import a project from GitHub."

    stdout = freshermeat.scripts.import_project_from_github(
        owner, repo, submitter_id
    )
    print(stdout)


@application.cli.command("import_project_from_gitlab")
@click.option("--repository", help="Repository")
@click.option("--submitter_id", help="Id of the submitter")
def import_project_from_gitlab(repository, submitter_id):
    "Import a project from GitLab."
    stdout = freshermeat.scripts.import_project_from_gitlab(
        repository, submitter_id
    )
    print(stdout)


@application.cli.command("import_osi_approved_licenses")
def import_osi_approved_licenses():
    "Import OSI approved licenses."
    print("Importing OSI approved licenses...")

    freshermeat.scripts.import_osi_approved_licenses()


@application.cli.command("fetch_cves")
@click.option("--cve_vendor", default=None)
def fetch_cves(cve_vendor):
    "Crawl the CVE."
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
    fetch_cve.retrieve(projects)
    end = datetime.now()

    logger.info(f"CVE fetcher finished in {(end - start).seconds} seconds.")


@application.cli.command("fetch_releases")
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


@application.cli.command("fetch_news")
def fetch_news():
    """Automatic news tracking
    Retrieves the new of the projects."""
    feeds = freshermeat.models.Feed.query.all()
    fetch_project_news.retrieve(feeds)
