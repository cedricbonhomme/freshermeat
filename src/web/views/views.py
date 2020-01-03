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

import os
import logging
from flask import (render_template, url_for, redirect, current_app, flash,
                  send_from_directory, request)
from werkzeug.contrib.atom import AtomFeed
from sqlalchemy import desc

from web.models import Release, Project, CVE, News
from bootstrap import application

logger = logging.getLogger(__name__)


@current_app.errorhandler(401)
def authentication_required(error):
    flash('Authentication required.', 'info')
    return redirect(url_for('login'))


@current_app.errorhandler(403)
def authentication_failed(error):
    flash('Forbidden.', 'danger')
    return redirect(url_for('login'))


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@current_app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500


@current_app.errorhandler(503)
def internal_server_error(error):
    return render_template('errors/503.html'), 503


@current_app.errorhandler(AssertionError)
def handle_sqlalchemy_assertion_error(error):
    return error.args[0], 400


@current_app.route('/public/<path:filename>', methods=['GET'])
def uploaded_pictures(filename='Ladybug.jpg', methods=['GET']):
    """
    Exposes public files (media uploaded by users, etc.).
    """
    return send_from_directory(os.path.abspath(application.config['UPLOAD_FOLDER']), filename)


@current_app.route('/', methods=['GET'])
def index():
    """Returns the home page."""
    nb_projects = Project.query.filter().count()
    nb_releases = Release.query.filter().count()
    nb_cves = CVE.query.filter().count()
    return render_template('index.html', nb_projects=nb_projects,
                            nb_releases=nb_releases, nb_cves=nb_cves)


@current_app.route('/releases.atom', methods=['GET'])
def recent_releases():
    """Generates a feed for the releases."""
    feed = AtomFeed('Recent releases',
                     feed_url=request.url, url=request.url_root)
    releases = Release.query.filter().order_by(desc(Release.published_at)).limit(100)
    for release in releases:
        feed.add('{} {}'.format(release.project.name, release.version),
                    release.changes,
                    id=release.id,
                    url=release.release_url,
                    updated=release.published_at)
    return feed.get_response()


@current_app.route('/cves.atom', methods=['GET'])
def recent_cves():
    """Generates a feed for the CVEs."""
    feed = AtomFeed('Recent CVEs',
                     feed_url=request.url, url=request.url_root)
    cves = CVE.query.filter().order_by(desc(CVE.published_at)).limit(100)
    for cve in cves:
        feed.add(cve.cve_id, cve.summary,
                 id=cve.id,
                 url='http://cve.circl.lu/cve/' + cve.cve_id,
                 updated=cve.published_at)
    return feed.get_response()


@current_app.route('/news.atom', methods=['GET'])
def recent_news():
    """Generates a feed for the news."""
    feed = AtomFeed('Recent news',
                     feed_url=request.url, url=request.url_root)
    news = News.query.filter().order_by(desc(News.published)).limit(100)
    for a_news in news:
        feed.add('{} - {}'.format(a_news.project.name, a_news.title),
                    a_news.content,
                    id=a_news.entry_id,
                    url=a_news.link,
                    updated=a_news.published)
    return feed.get_response()


@current_app.route('/about', methods=['GET'])
def about():
    """Returns the about page."""
    return render_template('about.html')
