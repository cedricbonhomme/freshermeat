#! /usr/bin/python
# -*- coding:utf-8 -*

import json

from web.models import Project, Organization, get_or_create
from bootstrap import db


def import_projects(json_file):
    with open(json_file) as json_file:
        projects = json.loads(json_file.read())

        for proj in projects:
            new_project = Project(
                        name=proj['name'],
                        short_description=proj['short_description'],
                        description=proj['description'],
                        website=proj['website'],
                        required_informations=proj.get('required_informations', None),
                        notification_email=proj.get('notification_email', None),
                        cve_vendor=proj.get('cve_vendor', ''),
                        cve_product=proj.get('cve_product', ''),
                        automatic_release_tracking=proj.get('automatic_release_tracking', ''))

            organization = get_or_create(db.session, Organization, **proj['organization'])

            new_project.organization_id = organization.id
            db.session.add(new_project)
        db.session.commit()
