#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from werkzeug import generate_password_hash
from bootstrap import application, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import and_

import web.models
import scripts
from workers import fetch_cve, fetch_release_github


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
def create_user(email, password):
    "Initializes a user"
    print("Creation of the user {} ...".format(email))
    with application.app_context():
        scripts.create_user(email, password, False)


@manager.command
def create_admin(email, password):
    "Initializes an admin user"
    print("Creation of the admin user {} ...".format(email))
    with application.app_context():
        scripts.create_user(email, password, True)


@manager.command
def import_projects(json_file):
    "Import projects from a JSON file"
    print("Importing projects from {} ...".format(json_file))
    with application.app_context():
        scripts.import_projects(json_file)


@manager.command
def fetch_cve_asyncio(cve_vendor=None):
    "Crawl the CVE with asyncio."
    import asyncio

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
    github_release = web.models.Project.query.filter(web.models.Project.automatic_release_tracking.like('github:%'))

    for project in github_release:
        fetch_release_github.fetch_release(project)



if __name__ == '__main__':
    manager.run()
