#! /usr/bin/python
import json

import requests

from freshermeat.bootstrap import application
from freshermeat.bootstrap import db
from freshermeat.models import Code
from freshermeat.models import License
from freshermeat.models import Project


def import_project_from_github(owner, repo, submitter_id):
    """Imports a project hosted from GitHub."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    url = "{api_url}?client_id={client_id}&client_secret={client_secret}".format(
        api_url=url,
        client_id=application.config.get("GITHUB_CLIENT_ID", ""),
        client_secret=application.config.get("GITHUB_CLIENT_SECRET", ""),
    )

    try:
        r = requests.get(url)
        project = json.loads(r.text)
    except Exception:
        return "ERROR:OBSCURE"

    if Project.query.filter(Project.name == project["name"]).first():
        return "ERROR:DUPLICATE_NAME"

    license = None
    try:
        spdx_id = project.get("license").get("spdx_id")
        if spdx_id:
            license = License.query.filter(License.license_id == spdx_id).first()
    except Exception:
        pass
    # if not license:
    # return 'ERROR:NO_LICENSE'

    new_project = Project(
        name=project["name"],
        short_description=project["description"],
        description=project["description"],
        website=project["html_url"],
        cve_vendor="",
        cve_product="",
        automatic_release_tracking="github:"
        + project.get("releases_url", "").replace("{/id}", ""),
        submitter_id=submitter_id,
    )

    if license:
        new_project.licenses.append(license)

    db.session.add(new_project)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return "ERROR:OBSCURE"

    new_code = Code(
        repository_url=project["clone_url"], scm_type="Git", project_id=new_project.id
    )
    db.session.add(new_code)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return "ERROR:OBSCURE"

    return new_project.name


def import_starred_projects_from_github(user, link=""):
    """Imports the starred projects of a GitHub user."""
    if link != "":
        url = link
    else:
        url = f"https://api.github.com/users/{user}/starred"
        url = "{api_url}?client_id={client_id}&client_secret={client_secret}".format(
            api_url=url,
            client_id=application.config.get("GITHUB_CLIENT_ID", ""),
            client_secret=application.config.get("GITHUB_CLIENT_SECRET", ""),
        )

    r = requests.get(url)
    starred = json.loads(r.text)

    for repo in starred:
        if repo["fork"]:
            continue
        new_project = Project(
            name=repo["name"],
            short_description=repo["description"],
            description=repo["description"],
            website=repo["html_url"],
            cve_vendor="",
            cve_product="",
            automatic_release_tracking="github:"
            + repo.get("releases_url", "").replace("{/id}", ""),
        )

        try:
            spdx_id = repo.get("license").get("spdx_id")
            if spdx_id:
                license = License.query.filter(License.license_id == spdx_id).first()
                if license:
                    new_project.licenses.append(license)
        except Exception:
            pass

        db.session.add(new_project)
        try:
            # names of projects are unique on freshermeat
            db.session.commit()
        except Exception:
            db.session.rollback()
            pass

    if r.links:
        import_starred_projects_from_github(user, r.links["next"]["url"])
