#! /usr/bin/python
# -*- coding:utf-8 -*

import json
import requests

from freshermeat.models import License
from freshermeat.bootstrap import db


def import_osi_approved_licenses():
    r = requests.get("https://spdx.org/licenses/licenses.json")
    if r.status_code == 200:
        result = json.loads(r.content)
        db.session.bulk_save_objects(
            [
                License(name=license["name"], license_id=license["licenseId"])
                for license in result["licenses"]
                if license["isOsiApproved"] and not license["isDeprecatedLicenseId"]
            ]
        )
        db.session.commit()
