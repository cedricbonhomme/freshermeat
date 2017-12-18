#! /usr/bin/env python
# -*- coding: utf-8 -

import json
import requests
from datetime import datetime
from sqlalchemy import and_

from bootstrap import db
from web.models import Release, get_or_create

def fetch_release(project):
    r = requests.get(project.automatic_release_tracking.split(':', 1)[1])
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
                                  download=release['tarball_url'],
                                  published_at=published_at,
                                  project_id=project.id)

            db.session.add(new_release)
    db.session.commit()
