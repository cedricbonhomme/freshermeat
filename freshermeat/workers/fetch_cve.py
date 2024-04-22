#! /usr/bin/env python
# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2024 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information: https://github.com/cedricbonhomme/freshermeat
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

import requests

from freshermeat.bootstrap import db
from freshermeat.models import CVE
from freshermeat.models import get_or_create

logger = logging.getLogger(__name__)

sem = asyncio.Semaphore(20)


async def get_cve(*args, **kwargs):
    try:
        request_kwargs = {
            "verify": True,
            "allow_redirects": True,
            "timeout": 15,
            "headers": {"User-Agent": "https://github.com/cedricbonhomme/freshermeat"},
        }
        result = requests.get(
            f"https://cvepremium.circl.lu/api/search/{args[0]}/{args[1]}",
            **request_kwargs,
        )
        logger.info(f"CVE for {args[2]} retrieved")
        if result.status_code == 200:
            if result.json()["total"] != 0:
                return result.json()["results"]
        return []
    except Exception as e:
        raise e


async def get_cve_vulnerability_lookup(*args, **kwargs):
    """
    Get recent CVEs for a product and a vendor by querying a vulnerability-lookup instance:
    https://vulnerability.circl.lu
    """
    try:
        request_kwargs = {
            "verify": True,
            "allow_redirects": True,
            "timeout": 15,
            "headers": {"User-Agent": "https://github.com/cedricbonhomme/freshermeat"},
        }
        result = requests.get(
            f"https://vulnerability.circl.lu/api/search/{args[0]}/{args[1]}",
            **request_kwargs,
        )
        logger.info(f"CVE for {args[2]} retrieved")
        if result.status_code == 200:
            return result.json()["cvelistv5"]
        return []
    except Exception as e:
        raise e


async def insert_database(project):
    async with sem:
        logger.info(f"Retrieving CVE for {project.name}")
        vendors = project.cve_vendor.split(",")
        for cve_vendor in vendors:
            cves = await get_cve(cve_vendor, project.cve_product, project.name)
            logger.info(f"Inserting CVE for {project.name}")
            for cve in cves:
                published_at = datetime.strptime(cve["Published"], "%Y-%m-%dT%H:%M:%S")

                get_or_create(
                    db.session,
                    CVE,
                    **{
                        "cve_id": cve["id"],
                        "summary": cve["summary"],
                        "published_at": published_at,
                        "project_id": project.id,
                    },
                )
    return cves


async def init_process(project):
    try:
        cves = await insert_database(project)
        return cves
    except Exception as e:
        logger.exception("init_process: " + str(e))


def retrieve(projects):
    """
    Launch the processus.
    """
    # Launch the process for all the projects
    logger.info("Retrieving CVEs...")
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(init_process(project)) for project in projects]
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception:
        logger.exception("an error occured")
    finally:
        loop.close()
        logger.info("CVEs retrieved")
