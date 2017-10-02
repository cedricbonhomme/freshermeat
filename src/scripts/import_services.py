#! /usr/bin/python
#-*- coding:utf-8 -*

import json

from web.models import Service
from bootstrap import db

def import_services(json_file):
    with open(json_file) as json_file:
        services = json.loads(json_file.read())

        for service in services:

            new_service = Service(name=service['name'],
                        short_description=service['short_description'],
                        description=service['description'],
                        logo=service['logo'],
                        webpage=service['webpage'],
                        required_informations=service['required_informations'])
            db.session.add(new_service)
        db.session.commit()
