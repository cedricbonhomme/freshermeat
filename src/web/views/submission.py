from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug import generate_password_hash
from bootstrap import db

from web.models import Submission
from web.forms import SubmissionForm


submissions_bp = Blueprint('submissions_bp', __name__,
                            url_prefix='/submissions')

@submissions_bp.route('/', methods=['GET'])
def list_submissions():
    """Return the page which will display the list of submissions."""
    head_titles = ['Submissions']
    return render_template('admin/submissions.html', head_titles=head_titles)
