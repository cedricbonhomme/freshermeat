from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug import generate_password_hash
from sqlalchemy import desc
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args
from bootstrap import db

from web.models import Submission
from web.forms import SubmissionForm


submissions_bp = Blueprint('submissions_bp', __name__,
                            url_prefix='/admin')

@submissions_bp.route('/submissions', methods=['GET'])
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
