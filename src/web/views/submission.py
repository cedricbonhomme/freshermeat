from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug import generate_password_hash
from sqlalchemy import desc
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args
from bootstrap import db

from web.views.common import admin_permission
from web.models import Submission, License
from web.forms import SubmissionForm


submissions_bp = Blueprint('submissions_bp', __name__, url_prefix='/admin')
submission_bp = Blueprint('submission_bp', __name__, url_prefix='/submit')

@submissions_bp.route('/submissions', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def list_submissions():
    """Return the page which will display the list of submissions."""
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
    """Return the submission given in parameter."""
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
    """Accept a submission."""
    pass


@submissions_bp.route('/submission/<int:submission_id>/toggle', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def toggle(submission_id=None):
    """Mark a submission as to be reviewed."""
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
    """Delete a submission."""
    submission = Submission.query.filter(Submission.id == submission_id).first()
    if submission is None:
        abort(404)
    db.session.delete(submission)
    db.session.commit()
    return redirect(url_for('submissions_bp.list_submissions'))


@submission_bp.route('/', methods=['GET'])
def form_submission():
    action = "Submit a project"
    head_titles = [action]
    form = SubmissionForm()
    return render_template('submit.html', action=action,
                           head_titles=head_titles, form=form)


@submission_bp.route('/', methods=['POST'])
def process_submission_form(user_id=None):
    form = SubmissionForm()

    if not form.validate():
        return render_template('submit.html', form=form)

    new_submission = Submission(project_name=form.project_name.data,
                           project_description=form.project_description.data,
                           project_website=form.project_website.data)
    db.session.add(new_submission)
    try:
        db.session.commit()
    except Exception as e:
        return redirect(url_for('submission_bp.form'))
    # Licenses
    new_licenses = []
    for license_id in form.licenses.data:
        license = License.query.filter(License.id == license_id).first()
        new_licenses.append(license)
    new_submission.licenses = new_licenses
    del form.licenses

    db.session.commit()
    flash('Your submission will be reviewed before publication.', 'success')

    return redirect(url_for('submission_bp.form_submission'))
