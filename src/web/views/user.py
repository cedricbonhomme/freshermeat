from flask import Blueprint, render_template
from flask_login import login_required

from web.views.common import admin_permission
from web.models import User


user_bp = Blueprint('user_bp', __name__, url_prefix='/admin/user')
users_bp = Blueprint('users_bp', __name__, url_prefix='/admin/users')
