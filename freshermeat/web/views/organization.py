#! /usr/bin/env python
# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2024 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information: https://github.com/cedricbonhomme/freshermeat
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
from datetime import timezone

from feedgen.feed import FeedGenerator
from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required

from freshermeat.bootstrap import application
from freshermeat.bootstrap import db
from freshermeat.models import Icon
from freshermeat.models import Organization
from freshermeat.web.forms import AddOrganizationForm
from freshermeat.web.views.common import admin_permission

organization_bp = Blueprint("organization_bp", __name__, url_prefix="/organization")
organizations_bp = Blueprint("organizations_bp", __name__, url_prefix="/organizations")


@organizations_bp.route("/", methods=["GET"])
def list_organizations():
    """Return the page which will display the list of organizations."""
    head_titles = ["Organizations"]
    return render_template("organizations.html", head_titles=head_titles)


@organization_bp.route("/<string:organization_name>", methods=["GET"])
def get(organization_name=None):
    """Return the organization given in parameter."""
    organization = Organization.query.filter(
        Organization.name == organization_name
    ).first()
    if organization is None:
        abort(404)
    head_titles = ["The " + organization.name + " Organization"]
    return render_template(
        "organization.html", organization=organization, head_titles=head_titles
    )


@organization_bp.route("/<string:organization_name>/releases.atom", methods=["GET"])
def recent_releases(organization_name=None):
    """Generates a feed for the releases of an organization."""
    organization = Organization.query.filter(
        Organization.name == organization_name
    ).first()
    if organization is None:
        abort(404)
    fg = FeedGenerator()
    fg.id(
        url_for(
            "organization_bp.recent_releases",
            organization_name=organization.name,
            _external=True,
        )
    )
    fg.title(f"Recent releases for {organization.name}")
    fg.link(href=request.url, rel="self")
    for project in organization.projects:
        for release in project.releases:
            fe = fg.add_entry()
            fe.id(f"{release.project.name} {release.version}")
            fe.title(f"{release.project.name} {release.version}")
            fe.description(release.changes)
            fe.link(href=release.release_url)
            fe.updated(release.published_at.replace(tzinfo=timezone.utc))
            fe.published(release.published_at.replace(tzinfo=timezone.utc))
    atomfeed = fg.atom_str(pretty=True)
    return atomfeed


@organization_bp.route("/create", methods=["GET"])
@organization_bp.route("/edit/<int:organization_id>", methods=["GET"])
@login_required
@admin_permission.require(http_exception=403)
def form(organization_id=None):
    """Returns a form for the creation/edition of organizations."""
    action = "Add an organization"
    head_titles = [action]

    form = AddOrganizationForm()

    if organization_id is None:
        return render_template(
            "edit_organization.html", action=action, head_titles=head_titles, form=form
        )

    organization = Organization.query.filter(Organization.id == organization_id).first()
    form = AddOrganizationForm(obj=organization)
    action = "Edit organization"
    head_titles = ["The " + organization.name + " organization", action]
    return render_template(
        "edit_organization.html",
        action=action,
        head_titles=head_titles,
        form=form,
        organization=organization,
    )


@organization_bp.route("/create", methods=["POST"])
@organization_bp.route("/edit/<int:organization_id>", methods=["POST"])
@login_required
@admin_permission.require(http_exception=403)
def process_form(organization_id=None):
    """Process the form for the creation/edition of organizations."""
    form = AddOrganizationForm()

    if not form.validate():
        return render_template("edit_organization.html", form=form)

    if organization_id is not None:
        organization = Organization.query.filter(
            Organization.id == organization_id
        ).first()
        # Logo
        f = form.logo.data
        if f:
            try:
                # Delete the previous icon
                icon_url = os.path.join(
                    application.config["UPLOAD_FOLDER"], organization.icon_url
                )
                os.unlink(icon_url)
                old_icon = Icon.query.filter(Icon.url == organization.icon_url).first()
                db.session.delete(old_icon)
                organization.icon_url = None
                db.session.commit()
            except Exception as e:
                print(e)

            # save the picture
            filename = str(uuid.uuid4()) + ".png"
            icon_url = os.path.join(application.config["UPLOAD_FOLDER"], filename)
            f.save(icon_url)
            # create the corresponding new icon object
            new_icon = Icon(url=filename)
            db.session.add(new_icon)
            db.session.commit()
            organization.icon_url = new_icon.url

        form.populate_obj(organization)
        try:
            db.session.commit()
            flash(
                "Organization {organization_name} successfully updated.".format(
                    organization_name=form.name.data
                ),
                "success",
            )
        except Exception:
            form.name.errors.append("Name already exists.")
        return redirect(
            url_for("organization_bp.form", organization_id=organization.id)
        )

    # Create a new organization
    new_organization = Organization(
        name=form.name.data,
        short_description=form.short_description.data,
        description=form.description.data,
        website=form.website.data,
        organization_type=form.organization_type.data,
        cve_vendor=form.cve_vendor.data,
    )
    db.session.add(new_organization)
    try:
        db.session.commit()
    except Exception:
        return redirect(
            url_for("organization_bp.form", organization_id=new_organization.id)
        )
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
        new_organization.icon_url = new_icon.url
    db.session.commit()
    flash(
        "Organization {organization_name} successfully created.".format(
            organization_name=new_organization.name
        ),
        "success",
    )

    return redirect(
        url_for("organization_bp.form", organization_id=new_organization.id)
    )
