#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2018  Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information : https://github.com/cedricbonhomme/Freshermeat
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

import asyncio
import logging
from datetime import datetime
from pycvesearch import CVESearch

from bootstrap import db
from web.models import CVE, get_or_create

logger = logging.getLogger(__name__)

sem = asyncio.Semaphore(20)

cve_search = CVESearch()


async def get_cve(*args, **kwargs):
    try:
        data = cve_search.search('{}/{}'.format(args[0], args[1]))
        logger.info('CVE for {} retrieved'.format(args[2]))
        return data
    except Exception as e:
        raise e


async def insert_database(project):
    with (await sem):
        logger.info('Retrieving CVE for {}'.format(project.name))
        vendors = project.cve_vendor.split(',')
        for cve_vendor in project.cve_vendor:
            cves = await get_cve(cve_vendor, project.cve_product, project.name)
            logger.info('Inserting CVE for {}'.format(project.name))
            for cve in cves:

                published_at = datetime.strptime(cve['Published'],
                                                 "%Y-%m-%dT%H:%M:%S.%f")

                get_or_create(db.session, CVE, **{'cve_id': cve['id'],
                                                  'summary': cve['summary'],
                                                  'published_at': published_at,
                                                  'project_id': project.id})
    return cves


async def init_process(project):
    try:
        cves = await insert_database(project)
        return cves
    except Exception as e:
        logger.exception('init_process: ' + str(e))


def retrieve(loop, projects):
    """
    Launch the processus.
    """
    # Launch the process for all the projects
    logger.info('Retrieving CVEs...')
    tasks = [asyncio.ensure_future(init_process(project)) for project in projects]
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception:
        logger.exception('an error occured')
    finally:
        logger.info('CVEs retrieved')
