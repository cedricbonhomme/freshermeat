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

import json
import requests
from datetime import datetime
from sqlalchemy import and_

from bootstrap import db, application
from web.models import Release, get_or_create


async def retrieve_changelog(queue, projects):
    pass

async def retrieve_github(queue, projects):
    for project in projects:
        print('Retrieving releases for {}'.format(project.name))
        url = '{api_url}?client_id={client_id}&client_secret={client_secret}'. \
                format(api_url=project.automatic_release_tracking.split(':', 1)[1],
                client_id=application.config.get('GITHUB_CLIENT_ID', ''),
                client_secret=application.config.get('GITHUB_CLIENT_SECRET', ''))
        try:
            r = requests.get(url)
        except Exception as e:
            print(e)
        await queue.put((project.id, json.loads(r.text)))
    await queue.put(None)

async def insert_releases(queue):
    while True:
        item = await queue.get()
        if item is None:
            break

        project_id, releases = item
        for release in releases:
            try:
                tag_name = release['tag_name']
            except Exception as e:
                print(e)
                continue
            if Release.query.filter(
                        and_(Release.project_id==project_id,
                            Release.version==tag_name)).count() == 0:
                try:
                    published_at = datetime.strptime(release['published_at'],
                                                     "%Y-%m-%dT%H:%M:%SZ")
                except:
                    published_at = datetime.utcnow()
                new_release = Release(version=release['tag_name'],
                                      changes=release['body'],
                                      release_url=release['html_url'],
                                      download_url=release['tarball_url'],
                                      published_at=published_at,
                                      project_id=project_id)

                db.session.add(new_release)
        db.session.commit()
