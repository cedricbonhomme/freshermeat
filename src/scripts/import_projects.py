#! /usr/bin/python
# -*- coding:utf-8 -*

import json

from web.models import Project, Code, Organization, Service, get_or_create
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
                        cve_vendor=proj.get('cve_vendor', ''),
                        cve_product=proj.get('cve_product', ''),
                        automatic_release_tracking=proj.get('automatic_release_tracking', ''))

            organization = get_or_create(db.session, Organization, **proj['organization'])

            for code_location in proj.get('code_locations', []):
                code = get_or_create(db.session, Code, **code_location)
                new_project.code_locations.append(code)


            services = proj.get('services', [])
            for service in services:
                new_service = Service(
                    name=service.get('name', ''),
                    description=service.get('description', ''),
                    notification_email=service.get('notification_email', ''),
                    required_informations=service.get('required_informations',
                                                      None))
                db.session.add(new_service)
                new_project.services.append(new_service)



            new_project.organization_id = organization.id
            db.session.add(new_project)
        db.session.commit()
