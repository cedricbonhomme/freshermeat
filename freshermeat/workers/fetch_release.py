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
import json
import random

import maya
import requests
from sqlalchemy import and_

from freshermeat.bootstrap import application
from freshermeat.bootstrap import db
from freshermeat.models import Release

TIMEOUT = 2


async def retrieve_changelog(queue, projects):
    pass


async def retrieve_gitlab(queue, projects):
    """Producer coro: retrieve releases from GitLab."""
    for project in projects:
        print(f"Retrieving releases for {project.name} (via GitLab coroutine)")
        api_url = project.automatic_release_tracking.split(":", 1)[1]
        try:
            r = requests.get(api_url, timeout=TIMEOUT)
        except Exception as e:
            print(e)
        if r.status_code != 200:
            continue
        tags = json.loads(r.text)

        # construct the list of releases for the consumer coroutine
        releases = []
        for tag in tags:
            if "release" in tag and tag["release"]:
                releases.append(
                    {
                        "tag_name": tag["release"]["tag_name"],
                        "body": tag["release"]["description"],
                        "published_at": tag["commit"]["authored_date"],
                        "html_url": "",
                        "tarball_url": "",
                    }
                )
        await queue.put((project.id, releases))
    await queue.put(None)


async def retrieve_github(queue, projects):
    """Producer coro: retrieve releases from GitHub."""
    headers = {
        # "client_id": application.config.get("GITHUB_CLIENT_ID", ""),
        # "client_secret": application.config.get("GITHUB_CLIENT_SECRET", ""),
        "Authorization": "Bearer {}".format(application.config.get("GITHUB_TOKEN", "")),
        "Accept": "application/vnd.github.v3+json",
    }
    all_projects = projects.all()
    random.shuffle(all_projects)
    for project in all_projects:
        print(f"Retrieving releases for {project.name} (via GitHub coroutine)")
        r, releases = None, []
        url = project.automatic_release_tracking.split(":", 1)[1]
        try:
            r = requests.get(url, headers=headers, timeout=TIMEOUT)
        except Exception:
            continue
        if not r and r.status_code != 200:
            print(r.reason)
            continue
        releases = json.loads(r.text)
        await queue.put((project.id, releases))
    await queue.put(None)


async def insert_releases(queue, nḅ_producers=2):
    """Consumer coro: insert new releases in the database."""
    nb_producers_done = 0
    while True:
        item = await queue.get()
        if item is None:
            nb_producers_done += 1
            if nb_producers_done == nḅ_producers:
                print("All producers done.")
                print("Process finished.")
                break
            continue

        project_id, releases = item
        for release in releases:
            try:
                tag_name = release["tag_name"]
            except Exception as e:
                print(e)
                continue
            # check if the release is not already in the database
            if (
                Release.query.filter(
                    and_(Release.project_id == project_id, Release.version == tag_name)
                ).count()
                == 0
            ):
                try:
                    published_at = maya.parse(release["published_at"]).datetime(
                        to_timezone="UTC", naive=True
                    )
                except Exception:
                    published_at = maya.now().datetime(to_timezone="UTC", naive=True)

                new_release = Release(
                    version=release["tag_name"],
                    changes=release["body"],
                    release_url=release["html_url"],
                    download_url=release["tarball_url"],
                    published_at=published_at,
                    project_id=project_id,
                )

                db.session.add(new_release)
        db.session.commit()
