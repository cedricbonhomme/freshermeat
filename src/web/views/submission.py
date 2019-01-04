#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2019  Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information : https://gitlab.com/cedric/Freshermeat
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

from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug import generate_password_hash
from sqlalchemy import desc
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args
from bootstrap import db

from web.views.common import admin_permission
from web.models import Submission, License, Project
from web.forms import SubmissionForm


submissions_bp = Blueprint('submissions_bp', __name__, url_prefix='/admin')
submission_bp = Blueprint('submission_bp', __name__, url_prefix='/submit')

@submissions_bp.route('/submissions', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def list_submissions():
    """Return a page which will displays a paginated list of submissions."""
    head_titles = ['Submissions']

    submissions = Submission.query

    page, per_page, offset = get_page_args()
    pagination = Pagination(page=page, total=submissions.count(),
                            css_framework='bootstrap4',
                            search=False, record_name='submissions',
                            per_page=per_page)

    return render_template('admin/submissions.html',
                            submissions=submissions. \
                                    order_by(desc(Submission.created_at)). \
                                    offset(offset). \
                                    limit(per_page), pagination=pagination)


@submissions_bp.route('/submission/<int:submission_id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def get(submission_id=None):
    """Return details about the submission given in parameter."""
    submission = Submission.query.filter(Submission.id == submission_id).first()
    if submission is None:
        abort(404)
    submission.reviewed = True
    db.session.commit()
    action = 'Submission details'
    head_titles = [action]
    return render_template('admin/submission.html', submission=submission,
                            action = action, head_titles=head_titles)


@submissions_bp.route('/submission/<int:submission_id>/accept', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def accept(submission_id=None):
    """Let an administrator accept a submission. In consequence this will
    create a new project and then redirects the administrator to the project
    edition page in order to finalize the creation."""
    submission = Submission.query.filter(Submission.id == submission_id).first()
    if submission is None:
        abort(404)
    new_project = Project(
                    name=submission.project_name,
                    short_description=submission.project_description,
                    description='',
                    website=submission.project_website)
    new_project.licenses = submission.licenses
    db.session.add(new_project)
    try:
        db.session.commit()
        flash('Project {project_name} successfully updated.'.
              format(project_name=new_project.name), 'success')
    except Exception as e:
        flash('Impossible to create the project.', 'danger')
        return redirect(url_for('submissions_bp.get',
                                submission_id=submission_id))
    return redirect(url_for('project_bp.form', project_id=new_project.id))


@submissions_bp.route('/submission/<int:submission_id>/toggle', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def toggle(submission_id=None):
    """Let an administrator mark a submission as to be reviewed."""
    submission = Submission.query.filter(Submission.id == submission_id).first()
    if submission is None:
        abort(404)
    submission.reviewed = False
    db.session.commit()
    return redirect(url_for('submissions_bp.list_submissions'))


@submissions_bp.route('/submission/<int:submission_id>/delete', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete(submission_id=None):
    """Let an administrator delete a submission."""
    submission = Submission.query.filter(Submission.id == submission_id).first()
    if submission is None:
        abort(404)
    db.session.delete(submission)
    db.session.commit()
    return redirect(url_for('submissions_bp.list_submissions'))


@submission_bp.route('/', methods=['GET'])
def form_submission():
    """Returns a form in order to let anyone submit a project."""
    action = "Submit a project"
    head_titles = [action]
    form = SubmissionForm()
    return render_template('submit.html', action=action,
                           head_titles=head_titles, form=form)


@submission_bp.route('/', methods=['POST'])
def process_submission_form():
    """Process the form for the new project submission."""
    form = SubmissionForm()

    if not form.validate():
        return render_template('submit.html', form=form)

    project = Project.query.filter(Project.name == form.project_name.data). \
                            first()
    if project is not None:
        flash('A project with the same name already exists.', 'danger')
        return redirect(url_for('submission_bp.process_submission_form'))

    new_submission = Submission(project_name=form.project_name.data,
                           project_description=form.project_description.data,
                           project_website=form.project_website.data)
    db.session.add(new_submission)
    try:
        db.session.commit()
    except Exception as e:
        print(e._message)
        flash('Impossible to create the project.', 'danger')
        return redirect(url_for('submission_bp.process_submission_form'))
    # Licenses
    for license_id in form.licenses.data:
        license = License.query.filter(License.id == license_id).first()
        new_submission.licenses.append(license)
    del form.licenses
    db.session.commit()
    flash('Thank you for your contribution. The submission will be reviewed' +
            ' before publication.', 'success')

    return redirect(url_for('submission_bp.form_submission'))
