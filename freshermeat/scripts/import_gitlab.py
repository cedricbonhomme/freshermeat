#! /usr/bin/python
# -*- coding:utf-8 -*

import json
import requests
from urllib.parse import urlparse

from freshermeat.models import Project, Tag
from freshermeat.bootstrap import db, application


def import_project_from_gitlab(repository, submitter_id):
    """Imports a project hosted from GitLab."""
    url_parts = urlparse(repository)
    gitlab_instance = url_parts.netloc
    owner, repo = url_parts.path.strip("/").split("/")

    url = "https://{gitlab_instance}/api/v4/projects/{owner}%2F{repo}".format(
        gitlab_instance=gitlab_instance, owner=owner, repo=repo
    )

    try:
        r = requests.get(url)
        project = json.loads(r.text)
    except:
        return "ERROR:OBSCURE"

    if Project.query.filter(Project.name == project["name"]).first():
        return "ERROR:DUPLICATE_NAME"

    automatic_release_tracking = "gitlab:{url}/repository/tags".format(url=url)

    new_project = Project(
        name=project["name"],
        short_description=project["description"],
        description=project["description"],
        website=project["web_url"],
        cve_vendor="",
        cve_product="",
        automatic_release_tracking=automatic_release_tracking,
        submitter_id=submitter_id,
    )

    db.session.add(new_project)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return "ERROR:OBSCURE"

    for tag in project["tag_list"]:
        new_tag = Tag(text=tag.strip(), project_id=new_project.id)
        db.session.add(new_tag)
    db.session.commit()

    return new_project.name
