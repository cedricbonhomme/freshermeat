#! /usr/bin/python
# -*- coding:utf-8 -*

import json
import requests

from web.models import Language, get_or_create
from bootstrap import db

def import_languages(json_file):
    with open(json_file) as json_file:
        languages = json.loads(json_file.read())
        for language in languages:
            get_or_create(db.session, Language, **language)
