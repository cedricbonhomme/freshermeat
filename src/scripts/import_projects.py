#! /usr/bin/python
# -*- coding:utf-8 -*

import json

from web.models import Project, Organization, get_or_create
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
                        notification_email=project['notification_email'],
                        cve_vendor=project.get('cve_vendor', ''),
                        cve_product=project.get('cve_product', ''),
                        automatic_release_tracking=project.get('automatic_release_tracking', ''))

            organization = get_or_create(db.session, Organization, **project['organization'])

            new_project.organization_id = organization.id
            db.session.add(new_project)
        db.session.commit()
