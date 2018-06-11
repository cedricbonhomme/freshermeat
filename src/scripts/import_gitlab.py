#! /usr/bin/python
# -*- coding:utf-8 -*

import json
import requests

from web.models import Project, License
from bootstrap import db, application


def import_project_from_gitlab(owner, repo, submitter_id):
    url = 'https://gitlab.com/api/v4/projects/{owner}%2F{repo}'. \
            format(owner=owner, repo=repo)

    try:
        r = requests.get(url)
        project = json.loads(r.text)
    except:
        return 'ERROR:OBSCURE'

    if Project.query.filter(Project.name == project['name']).first():
        return 'ERROR:DUPLICATE_NAME'

    new_project = Project(
                    name=project['name'],
                    short_description=project['description'],
                    description=project['description'],
                    website=project['web_url'],
                    cve_vendor='',
                    cve_product='',
                    automatic_release_tracking='',
                    submitter_id=submitter_id)

    db.session.add(new_project)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return 'ERROR:OBSCURE'

    return new_project.name
