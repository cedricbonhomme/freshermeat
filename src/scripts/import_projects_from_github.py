#! /usr/bin/python
# -*- coding:utf-8 -*

import json
import requests

from web.models import Project
from bootstrap import db


def import_projects_from_github(user, link=''):
    if link != '':
        r = requests.get(link)
    else:
        r = requests.get('https://api.github.com/users/{user}/starred'
                         .format(user=user))

    starred = json.loads(r.text)

    for repo in starred:
        if repo['fork']:
            continue
        new_project = Project(
                    name=repo['name'],
                    short_description=repo['description'],
                    description=repo['description'],
                    website=repo['html_url'],
                    service_enabled=False,
                    required_informations=None,
                    notification_email=None,
                    cve_vendor='',
                    cve_product='',
                    automatic_release_tracking='github:' + repo.get('releases_url', '').replace('{/id}', ''))

        db.session.add(new_project)
        try:
            # names of projects are unique on freshermeat
            db.session.commit()
        except:
            pass

    if r.links:
        import_projects_from_github(user, r.links['next']['url'])
