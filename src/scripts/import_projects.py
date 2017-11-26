#! /usr/bin/python
# -*- coding:utf-8 -*

import json

from web.models import Project
from bootstrap import db


def import_projects(json_file):
    with open(json_file) as json_file:
        projects = json.loads(json_file.read())

        for project in projects:
            new_project = Project(
                        name=project['name'],
                        short_description=project['short_description'],
                        description=project['description'],
                        website=project['website'],
                        required_informations=project['required_informations'],
                        notification_email=project['notification_email'])
            db.session.add(new_project)
        db.session.commit()
