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
