#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import asyncio
from datetime import datetime
from werkzeug import generate_password_hash
from bootstrap import application, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import and_

import web.models
import scripts
from workers import fetch_cve, fetch_release


logger = logging.getLogger('manager')

Migrate(application, db)
manager = Manager(application)
manager.add_command('db', MigrateCommand)


@manager.command
def db_empty():
    "Will drop every datas stocked in db."
    with application.app_context():
        web.models.db_empty(db)


@manager.command
def db_create():
    "Will create the database."
    with application.app_context():
        web.models.db_create(db, application.config['DB_CONFIG_DICT'],
                             application.config['DATABASE_NAME'])


@manager.command
def db_init():
    "Will create the database from conf parameters."
    with application.app_context():
        web.models.db_init(db)


@manager.command
def create_user(login, email, password):
    "Initializes a user"
    print("Creation of the user {} ...".format(login))
    with application.app_context():
        scripts.create_user(login, email, password, False)


@manager.command
def create_admin(login, email, password):
    "Initializes an admin user"
    print("Creation of the admin user {} ...".format(login))
    with application.app_context():
        scripts.create_user(login, email, password, True)


@manager.command
def import_projects(json_file):
    "Import projects from a JSON file"
    print("Importing projects from {} ...".format(json_file))
    with application.app_context():
        scripts.import_projects(json_file)


@manager.command
def import_projects_from_github(user):
    "Import GitHub starred projects of a user."
    print("Importing GitHub starred projects of {} ...".format(user))
    with application.app_context():
        scripts.import_projects_from_github(user)


@manager.command
def import_osi_approved_licenses():
    "Import OSI approved licenses."
    print("Importing OSI approved licenses...")
    with application.app_context():
        scripts.import_osi_approved_licenses()


@manager.command
def fetch_cve_asyncio(cve_vendor=None):
    "Crawl the CVE with asyncio."

    with application.app_context():

        query = web.models.Project.query.filter(
                                    and_(web.models.Project.cve_vendor != '',
                                         web.models.Project.cve_product != ''))
        if cve_vendor:
            query = query.filter(web.models.Project.cve_vendor == cve_vendor)
        projects = query.all()

        logger.info('Starting CVE fetcher.')

        start = datetime.now()
        loop = asyncio.get_event_loop()
        fetch_cve.retrieve(loop, projects)
        loop.close()
        end = datetime.now()

        logger.info('CVE fetcher finished in {} seconds.' \
            .format((end - start).seconds))


@manager.command
def fetch_releases():
    """Automatic release tracking
    Retrieves the new releases of the projects."""
    github_releases = web.models.Project.query.filter(
            web.models.Project.automatic_release_tracking.like('github:%'))
    changelog_releases = web.models.Project.query.filter(
            web.models.Project.automatic_release_tracking.like('changelog:%'))

    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(maxsize=5, loop=loop)

    producer_coro_github = fetch_release.retrieve_github(queue, github_releases)
    producer_coro_changelog = fetch_release.retrieve_changelog(queue,
                                                            changelog_releases)
    consumer_coro = fetch_release.insert_releases(queue)

    loop.run_until_complete(asyncio.gather(producer_coro_github,
                                           producer_coro_changelog,
                                           consumer_coro))
    loop.close()



if __name__ == '__main__':
    manager.run()
