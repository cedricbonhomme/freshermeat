#! /usr/bin/env python
# -*- coding: utf-8 -

import json
import requests
from datetime import datetime
from sqlalchemy import and_

from bootstrap import db, application
from web.models import Release, get_or_create

def fetch_release(project):
    url = '{api_url}?client_id={client_id}&client_secret={client_secret}'. \
        format(api_url=project.automatic_release_tracking.split(':', 1)[1],
            client_id=application.config.get('GITHUB_CLIENT_ID', ''),
            client_secret=application.config.get('GITHUB_CLIENT_SECRET', ''))
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
    #assert r.status_code == 200, 'Error Code: {}\nError message: {}'.format(r.status_code, r.text)
    releases = json.loads(r.text)
    for release in releases:
        if Release.query.filter(
                    and_(Release.project_id==project.id,
                        Release.version==release['tag_name'])).count() == 0:
            try:
                published_at = datetime.strptime(release['published_at'], "%Y-%m-%dT%H:%M:%SZ")
            except:
                published_at = datetime.utcnow()
            new_release = Release(version=release['tag_name'],
                                  changes=release['body'],
                                  release_url=release['html_url'],
                                  download_url=release['tarball_url'],
                                  published_at=published_at,
                                  project_id=project.id)

            db.session.add(new_release)
    db.session.commit()
