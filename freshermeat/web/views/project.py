#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2021 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information: https://sr.ht/~cedric/freshermeat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

# from werkzeug.contrib.atom import AtomFeed

from freshermeat.bootstrap import db, application
from freshermeat.models import (
    get_or_create,
    Project,
    Code,
    Organization,
    Tag,
    Icon,
    License,
    Language,
    Feed,
)
from freshermeat.web.forms import AddProjectForm, CodeForm, FeedForm
from freshermeat.web.utils.misc import similar_projects
from freshermeat.web.utils.spawn import ERRORS, import_github, import_gitlab

project_bp = Blueprint("project_bp", __name__, url_prefix="/project")
projects_bp = Blueprint("projects_bp", __name__, url_prefix="/projects")


@projects_bp.route("/", methods=["GET"])
def list_projects():
    """Return the page which will display the list of projects."""
    head_titles = ["Projects"]
    return render_template("projects.html", head_titles=head_titles)


@project_bp.route("/<string:project_name>", methods=["GET"])
def get(project_name=None):
    """Return the project given in parameter."""
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    similar = similar_projects(project)
    head_titles = ["The " + project.name + " Open Source Project"]
    return render_template(
        "project.html", project=project, similar=similar, head_titles=head_titles
    )


@project_bp.route("/<string:project_name>/delete", methods=["GET"])
@login_required
def delete(project_name=None):
    """Delete a project."""
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted.", "success")
    return redirect(url_for("projects_bp.list_projects"))


@project_bp.route("/<string:project_name>/settings", methods=["GET"])
def settings(project_name=None):
    """Return the settings page."""
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    head_titles = ["The " + project.name + " Open Source Project", "Settings Page"]
    return render_template("settings.html", project=project, head_titles=head_titles)


@project_bp.route("/<string:project_name>/code", methods=["GET"])
def code_locations(project_name=None):
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    form = CodeForm()
    return render_template("code.html", project=project, form=form)


@project_bp.route("/<string:project_name>/code", methods=["POST"])
@login_required
def code_locations_process(project_name=None):
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    form = CodeForm()
    if not form.validate():
        return render_template("code.html", project=project, form=form)
    new_code = Code(
        repository_url=form.repository_url.data,
        scm_type=form.scm_type.data,
        project_id=project.id,
    )
    db.session.add(new_code)
    try:
        db.session.commit()
        flash("New location successfully created.", "success")
    except Exception as e:
        flash("Impossible to add a new location.", "success")
    return render_template("code.html", project=project, form=form)


@project_bp.route("/<string:project_name>/releases", methods=["GET"])
def edit_releases(project_name=None):
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    return render_template("edit_releases.html", project=project)


@project_bp.route("/<string:project_name>/feeds", methods=["GET"])
def feed(project_name=None):
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    feeds = Feed.query.filter(Feed.project_id == project.id)
    form = FeedForm()
    return render_template("feed.html", project=project, feeds=feeds, form=form)


@project_bp.route("/<string:project_name>/feeds", methods=["POST"])
@login_required
def feed_locations_process(project_name=None):
    """Process the new f"""
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    feeds = Feed.query.filter(Feed.project_id == project.id)
    form = FeedForm()
    if not form.validate():
        return render_template("feed.html", project=project, feeds=feeds, form=form)
    new_feed = Feed(link=form.link.data, project_id=project.id)
    db.session.add(new_feed)
    try:
        db.session.commit()
        flash("New feed successfully created.", "success")
    except Exception as e:
        flash("Impossible to add a new feed.", "success")
    return render_template("feed.html", project=project, feeds=feeds, form=form)


@project_bp.route("/<string:project_name>/releases.atom", methods=["GET"])
def recent_releases(project_name=None):
    """Generates a feed for the releases."""
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    feed = AtomFeed(
        "Recent releases for {}".format(project.name),
        feed_url=request.url,
        url=request.url_root,
    )
    for release in project.releases:
        feed.add(
            "{} {}".format(release.project.name, release.version),
            release.changes,
            id=release.id,
            url=release.release_url,
            updated=release.published_at,
        )
    return feed.get_response()


@project_bp.route("/<string:project_name>/cves.atom", methods=["GET"])
def recent_cves(project_name=None):
    """Generates a feed for the CVEs."""
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    feed = AtomFeed(
        "Recent CVEs for {}".format(project.name),
        feed_url=request.url,
        url=request.url_root,
    )
    for cve in project.cves:
        feed.add(
            cve.cve_id,
            cve.summary,
            id=cve.id,
            url="http://cve.circl.lu/cve/" + cve.cve_id,
            updated=cve.published_at,
        )
    return feed.get_response()


@project_bp.route("/<string:project_name>/news.atom", methods=["GET"])
def recent_news(project_name=None):
    """Generates a feed for the news."""
    project = Project.query.filter(Project.name == project_name).first()
    if project is None:
        abort(404)
    feed = AtomFeed(
        "Recent news for {}".format(project.name),
        feed_url=request.url,
        url=request.url_root,
    )
    for news in project.news:
        feed.add(
            "{}".format(news.title),
            news.content,
            id=news.entry_id,
            url=news.link,
            updated=news.published,
        )
    return feed.get_response()


@project_bp.route("/create", methods=["GET"])
@project_bp.route("/edit/<int:project_id>", methods=["GET"])
@login_required
def form(project_id=None):
    """Returns a form for the creation/edition of projects."""
    action = "Add a project"
    head_titles = [action]

    form = AddProjectForm()
    form.organization_id.choices = [(0, "")]
    form.organization_id.choices.extend(
        [(org.id, org.name) for org in Organization.query.all()]
    )

    # Create a new project
    if project_id is None:
        return render_template(
            "edit_project.html", action=action, head_titles=head_titles, form=form
        )
    # Edit an existing project
    project = Project.query.filter(Project.id == project_id).first()
    form = AddProjectForm(obj=project)
    form.organization_id.choices = [(0, "")]
    form.organization_id.choices.extend(
        [(org.id, org.name) for org in Organization.query.all()]
    )
    form.licenses.data = [license.id for license in project.licenses]
    form.languages.data = [language.id for language in project.languages]
    form.dependencies.data = [dep.id for dep in project.dependencies]
    form.dependents.data = [dep.id for dep in project.dependents]
    form.tags.data = ", ".join(project.tags)
    action = "Edit project"
    head_titles = ["The " + project.name + " Open Source Project", action]
    return render_template(
        "edit_project.html",
        action=action,
        head_titles=head_titles,
        form=form,
        project=project,
    )


@project_bp.route("/create", methods=["POST"])
@project_bp.route("/edit/<int:project_id>", methods=["POST"])
@login_required
def process_form(project_id=None):
    """Process the form for the creation/edition of projects."""
    form = AddProjectForm()
    form.organization_id.choices = [(0, "")]
    form.organization_id.choices.extend(
        [(org.id, org.name) for org in Organization.query.all()]
    )

    if not form.validate():
        return render_template("edit_project.html", form=form)

    if form.organization_id.data == 0:
        form.organization_id.data = None

    if not current_user.is_admin:
        del form.organization_id

    # Edit an existing project
    if project_id is not None:
        project = Project.query.filter(Project.id == project_id).first()

        # Tags
        new_tags = [
            tag for tag in form.tags.data.strip().split(",") if tag and tag.strip()
        ]
        for tag in project.tag_objs:
            if tag.text not in new_tags:
                db.session.delete(tag)
        db.session.commit()
        for tag in new_tags:
            get_or_create(
                db.session, Tag, **{"text": tag.strip(), "project_id": project.id}
            )
        del form.tags

        # Licenses
        new_licenses = []
        for license_id in form.licenses.data:
            license = License.query.filter(License.id == license_id).first()
            new_licenses.append(license)
        project.licenses = new_licenses
        del form.licenses

        # Languages
        new_languages = []
        for language_id in form.languages.data:
            language = Language.query.filter(Language.id == language_id).first()
            new_languages.append(language)
        project.languages = new_languages
        del form.languages

        # dependencies
        new_projects = []
        for cur_project_id in form.dependencies.data:
            project_dep = Project.query.filter(Project.id == cur_project_id).first()
            new_projects.append(project_dep)
        project.dependencies = new_projects
        del form.dependencies

        # dependents
        new_projects = []
        for cur_project_id in form.dependents.data:
            project_dep = Project.query.filter(Project.id == cur_project_id).first()
            new_projects.append(project_dep)
        project.dependents = new_projects
        del form.dependents

        # Logo
        f = form.logo.data
        if f:
            try:
                # Delete the previous icon
                icon_url = os.path.join(
                    application.config["UPLOAD_FOLDER"], project.icon_url
                )
                os.unlink(icon_url)
                old_icon = Icon.query.filter(Icon.url == project.icon_url).first()
                db.session.delete(old_icon)
                project.icon_url = None
                db.session.commit()
            except Exception as e:
                pass

            # save the picture
            filename = str(uuid.uuid4()) + ".png"
            icon_url = os.path.join(application.config["UPLOAD_FOLDER"], filename)
            f.save(icon_url)
            # create the corresponding new icon object
            new_icon = Icon(url=filename)
            db.session.add(new_icon)
            db.session.commit()
            project.icon_url = new_icon.url

        form.populate_obj(project)
        try:
            db.session.commit()
            flash(
                "Project {project_name} successfully updated.".format(
                    project_name=form.name.data
                ),
                "success",
            )
        except Exception as e:
            form.name.errors.append("Name already exists.")
        return redirect(url_for("project_bp.form", project_id=project.id))

    # Create a new project
    new_project = Project(
        name=form.name.data,
        short_description=form.short_description.data,
        description=form.description.data,
        website=form.website.data,
        organization_id=form.organization_id.data,
        submitter_id=current_user.id,
    )
    db.session.add(new_project)
    try:
        db.session.commit()
    except Exception as e:
        # TODO: display the error
        return redirect(url_for("project_bp.form", project_id=new_project.id))
    # Tags
    for tag in form.tags.data.split(","):
        if tag.strip():
            get_or_create(
                db.session, Tag, **{"text": tag.strip(), "project_id": new_project.id}
            )

    # Licenses
    new_licenses = []
    for license_id in form.licenses.data:
        license = License.query.filter(License.id == license_id).first()
        new_licenses.append(license)
    new_project.licenses = new_licenses
    del form.licenses

    # Languages
    new_languages = []
    for language_id in form.languages.data:
        language = Language.query.filter(Language.id == language_id).first()
        new_languages.append(language)
    new_project.languages = new_languages
    del form.languages

    # dependencies
    new_projects = []
    for cur_project_id in form.dependencies.data:
        project_dep = Project.query.filter(Project.id == cur_project_id).first()
        new_projects.append(project_dep)
    new_project.dependencies = new_projects
    del form.dependencies

    # dependents
    new_projects = []
    for cur_project_id in form.dependents.data:
        project_dep = Project.query.filter(Project.id == cur_project_id).first()
        new_projects.append(project_dep)
    new_project.dependents = new_projects
    del form.dependents

    # Logo
    f = form.logo.data
    if f:
        # save the picture
        filename = str(uuid.uuid4()) + ".png"
        icon_url = os.path.join(application.config["UPLOAD_FOLDER"], filename)
        f.save(icon_url)
        # create the corresponding new icon object
        new_icon = Icon(url=filename)
        db.session.add(new_icon)
        new_project.icon_url = new_icon.url
    db.session.commit()
    flash(
        "Project {project_name} successfully created.".format(
            project_name=new_project.name
        ),
        "success",
    )

    return redirect(url_for("project_bp.form", project_id=new_project.id))


@project_bp.route("/import/<string:import_from>", methods=["GET"])
@login_required
def import_project(import_from=None):
    result = None

    if import_from in ["github", "gitlab"]:
        repository = request.args.get("project", None)
        if repository:
            try:
                result = globals()["import_" + import_from](repository, current_user.id)
                result = result.split()[0]
                # if the import is successful result is the name of the repo
            except Exception as e:
                print(e)
    else:
        abort(404)

    if not result:
        flash("Impossible to import the project.", "danger")
        return redirect(url_for("projects_bp.list_projects"))

    result = result.decode()
    if "ERROR" in result:
        error_description = ERRORS[result]
        flash("{error}".format(error=error_description), "danger")

        if "DUPLICATE_NAME" in result:
            return redirect(url_for("project_bp.get", project_name=result))
        return redirect(url_for("projects_bp.list_projects"))

    return redirect(url_for("project_bp.get", project_name=result))


@project_bp.route("/bookmarklet", methods=["GET", "POST"])
@login_required
def bookmarklet():
    url = (request.args if request.method == "GET" else request.form).get("url", None)
    if not url:
        flash(gettext("Couldn't add project: url missing."), "error")
        raise BadRequest("url is missing")

    name = (request.args if request.method == "GET" else request.form).get("name", "")

    action = "Add a project"
    head_titles = [action]

    form = AddProjectForm()
    form.organization_id.choices = [(0, "")]
    form.organization_id.choices.extend(
        [(org.id, org.name) for org in Organization.query.all()]
    )

    form.website.data = url
    form.name.data = name

    return render_template(
        "edit_project.html", action=action, head_titles=head_titles, form=form
    )
