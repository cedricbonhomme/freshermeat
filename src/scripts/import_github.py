#! /usr/bin/python
# -*- coding:utf-8 -*

import json
import requests

from web.models import Project, License
from bootstrap import db, application


def import_project_from_github(owner, repo):
    url = 'https://api.github.com/repos/{owner}/{repo}'.format(owner=owner,
                                                                repo=repo)
    url = '{api_url}?client_id={client_id}&client_secret={client_secret}'. \
            format(api_url=url,
            client_id=application.config.get('GITHUB_CLIENT_ID', ''),
            client_secret=application.config.get('GITHUB_CLIENT_SECRET', ''))

    r = requests.get(url)
    project = json.loads(r.text)

    new_project = Project(
                    name=project['name'],
                    short_description=project['description'],
                    description=project['description'],
                    website=project['html_url'],
                    cve_vendor='',
                    cve_product='',
                    automatic_release_tracking='github:' + project.get('releases_url', '').replace('{/id}', ''))

    try:
        spdx_id = project.get('license').get('spdx_id')
        if spdx_id:
            license = License.query.filter(License.license_id==spdx_id).first()
            if license:
                new_project.licenses.append(license)
    except:
        pass

    # print(new_project)
    db.session.add(new_project)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        pass
