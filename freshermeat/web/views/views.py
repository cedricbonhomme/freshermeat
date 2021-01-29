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
import logging
from datetime import timezone
from flask import (
    render_template,
    url_for,
    redirect,
    current_app,
    flash,
    send_from_directory,
    request,
)

from sqlalchemy import desc
from feedgen.feed import FeedGenerator

from freshermeat.models import Release, Project, CVE, News
from freshermeat.bootstrap import application

logger = logging.getLogger(__name__)


@current_app.errorhandler(401)
def authentication_required(error):
    flash("Authentication required.", "info")
    return redirect(url_for("login"))


@current_app.errorhandler(403)
def authentication_failed(error):
    flash("Forbidden.", "danger")
    return redirect(url_for("login"))


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@current_app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500


@current_app.errorhandler(503)
def internal_server_error(error):
    return render_template("errors/503.html"), 503


@current_app.errorhandler(AssertionError)
def handle_sqlalchemy_assertion_error(error):
    return error.args[0], 400


@current_app.route("/public/<path:filename>", methods=["GET"])
def uploaded_pictures(filename="Ladybug.jpg", methods=["GET"]):
    """
    Exposes public files (media uploaded by users, etc.).
    """
    return send_from_directory(
        os.path.abspath(application.config["UPLOAD_FOLDER"]), filename
    )


@current_app.route("/", methods=["GET"])
def index():
    """Returns the home page."""
    nb_projects = Project.query.filter().count()
    nb_releases = Release.query.filter().count()
    nb_cves = CVE.query.filter().count()
    return render_template(
        "index.html", nb_projects=nb_projects, nb_releases=nb_releases, nb_cves=nb_cves
    )


@current_app.route("/releases.atom", methods=["GET"])
def recent_releases():
    """Generates a feed for the releases."""
    fg = FeedGenerator()
    fg.id(url_for("recent_releases", _external=True))
    fg.title("Recent releases")
    fg.link(href=request.url, rel="self")
    releases = Release.query.filter().order_by(desc(Release.published_at)).limit(100)
    for release in releases:
        fe = fg.add_entry()
        fe.id("{} {}".format(release.project.name, release.version))
        fe.title("{} {}".format(release.project.name, release.version))
        fe.description(release.changes)
        fe.link(href=release.release_url)
        fe.updated(release.published_at.replace(tzinfo=timezone.utc))
        fe.published(release.published_at.replace(tzinfo=timezone.utc))
    atomfeed = fg.atom_str(pretty=True)
    return atomfeed


@current_app.route("/cves.atom", methods=["GET"])
def recent_cves():
    """Generates a feed for the CVEs."""
    fg = FeedGenerator()
    fg.id(url_for("recent_cves", _external=True))
    fg.title("Recent CVEs")
    fg.link(href=request.url, rel="self")
    cves = CVE.query.filter().order_by(desc(CVE.published_at)).limit(100)
    for cve in cves:
        fe = fg.add_entry()
        fe.id(cve.cve_id)
        fe.title("{} - {}".format(cve.project.name, cve.cve_id))
        fe.description(cve.summary)
        fe.link(href="https://cve.circl.lu/cve/" + cve.cve_id)
        fe.updated(cve.published_at.replace(tzinfo=timezone.utc))
        fe.published(cve.published_at.replace(tzinfo=timezone.utc))
    atomfeed = fg.atom_str(pretty=True)
    return atomfeed


@current_app.route("/news.atom", methods=["GET"])
def recent_news():
    """Generates a feed for the news."""
    fg = FeedGenerator()
    fg.id(url_for("recent_news", _external=True))
    fg.title("Recent news")
    fg.link(href=request.url, rel="self")
    news = News.query.filter().order_by(desc(News.published)).limit(100)
    for a_news in news:
        fe = fg.add_entry()
        fe.id(a_news.entry_id)
        fe.title("{} - {}".format(a_news.project.name, a_news.title))
        fe.description(a_news.content)
        fe.link(href=a_news.link)
        fe.updated(a_news.published_at.replace(tzinfo=timezone.utc))
        fe.published(a_news.published_at.replace(tzinfo=timezone.utc))
    atomfeed = fg.atom_str(pretty=True)
    return atomfeed


@current_app.route("/about", methods=["GET"])
def about():
    """Returns the about page."""
    return render_template("about.html")
