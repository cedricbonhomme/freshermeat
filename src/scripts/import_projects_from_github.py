#! /usr/bin/python
# -*- coding:utf-8 -*

import json
import requests

from web.models import Project, License
from bootstrap import db, application


def import_projects_from_github(user, link=''):
    if link != '':
        url = link
    else:
        url = 'https://api.github.com/users/{user}/starred'.format(user=user)
        url = '{api_url}?client_id={client_id}&client_secret={client_secret}'. \
                format(api_url=url,
                client_id=application.config.get('GITHUB_CLIENT_ID', ''),
                client_secret=application.config.get('GITHUB_CLIENT_SECRET', ''))

    r = requests.get(url)
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


        try:
            spdx_id = repo.get('license').get('spdx_id')
            if spdx_id:
                license = License.query.filter(License.license_id==spdx_id).first()
                if license:
                    new_project.licenses.append(license)
        except:
            pass


        db.session.add(new_project)
        try:
            # names of projects are unique on freshermeat
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            pass

    if r.links:
        import_projects_from_github(user, r.links['next']['url'])
