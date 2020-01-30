#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2020 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information: https://git.sr.ht/~cedric/freshermeat
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

from flask import Blueprint, render_template, jsonify
from datetime import datetime
from datetime import timedelta
from sqlalchemy import func

from freshermeat.bootstrap import db
from freshermeat.models import Project, License, Tag, Language, Organization, User

stats_bp = Blueprint("stats_bp", __name__, url_prefix="/stats")


@stats_bp.route("/", methods=["GET"])
def stats():
    """Returns a pages which displays global statistics about all projects."""
    head_titles = ["Statistics"]
    return render_template("stats.html", head_titles=head_titles)


@stats_bp.route("/licenses.json", methods=["GET"])
@stats_bp.route("/<string:organization_name>/licenses.json", methods=["GET"])
def licenses(organization_name=None):
    """Returns a JSON with the repartition of licenses per projects."""
    query = (
        db.session.query(License.name, func.count(License.id))
        .join(License.projects)
        .group_by(License.id)
    )
    if organization_name:
        org = Organization.query.filter(Organization.name == organization_name).first()
        if org:
            query = query.filter(Project.organization_id == org.id)
    result = query.all()
    return jsonify(dict(result))


@stats_bp.route("/languages.json", methods=["GET"])
@stats_bp.route("/<string:organization_name>/languages.json", methods=["GET"])
def languages(organization_name=None):
    """Returns a JSON with the repartition of languages per projects."""
    query = (
        db.session.query(Language.name, func.count(Language.id))
        .join(Language.projects)
        .group_by(Language.id)
    )
    if organization_name:
        org = Organization.query.filter(Organization.name == organization_name).first()
        if org:
            query = query.filter(Project.organization_id == org.id)
    result = query.all()
    return jsonify(dict(result))


@stats_bp.route("/tags.json", methods=["GET"])
def tags():
    """Returns a JSON with the repartition of tags per projects."""
    result = (
        db.session.query(func.lower(Tag.text), func.count(func.lower(Tag.text)))
        .group_by(func.lower(Tag.text))
        .all()
    )
    return jsonify(dict(result))


@stats_bp.route("/organizations.json", methods=["GET"])
def organizations():
    """Returns a JSON with the different types of organizations (Non-profit, Governmental, etc.)."""
    result = (
        db.session.query(
            Organization.organization_type, func.count(Organization.organization_type)
        )
        .group_by(Organization.organization_type)
        .all()
    )
    return jsonify(dict(result))


@stats_bp.route("/activity.json", methods=["GET"])
@stats_bp.route("/<string:organization_name>/activity.json", methods=["GET"])
def activity(organization_name=None):
    """Returns a JSON with the number of projects sorted by activity (by
    period of weeks).
    This function builds a dictionary of queries per time frame.
    """
    now = datetime.today()
    result = {}
    result["less than 1 month"] = db.session.query(Project).filter(
        Project.last_updated >= now - timedelta(weeks=4)
    )
    result["between 1 and 3 months"] = db.session.query(Project).filter(
        Project.last_updated.between(
            now - timedelta(weeks=13), now - timedelta(weeks=4)
        )
    )
    result["between 3 and 6 months"] = db.session.query(Project).filter(
        Project.last_updated.between(
            now - timedelta(weeks=26), now - timedelta(weeks=13)
        )
    )
    result["between 6 months and 1 year"] = db.session.query(Project).filter(
        Project.last_updated.between(
            now - timedelta(weeks=52), now - timedelta(weeks=26)
        )
    )
    result["between 1 and 2 years"] = db.session.query(Project).filter(
        Project.last_updated.between(
            now - timedelta(weeks=104), now - timedelta(weeks=52)
        )
    )
    result["more than 2 years"] = db.session.query(Project).filter(
        Project.last_updated <= now - timedelta(weeks=104)
    )

    if organization_name:
        org = Organization.query.filter(Organization.name == organization_name).first()
        if org:
            for query in result:
                result[query] = result[query].filter(Project.organization_id == org.id)

    for query in result:
        result[query] = result[query].count()

    return jsonify(result)


@stats_bp.route("/submitters.json", methods=["GET"])
def submitters():
    """Returns a JSON with the repartition of submitters."""
    result = (
        db.session.query(User.login, func.count(User.id))
        .join(User.contributions)
        .group_by(User.id)
        .all()
    )
    return jsonify(dict(result))
