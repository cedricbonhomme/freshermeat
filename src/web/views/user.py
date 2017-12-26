from flask import Blueprint, render_template

from web.models import User


user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@user_bp.route('/<string:login>', methods=['GET'])
def get(login=None):
    user = User.query.filter(User.login == login).first()
    return render_template('user.html', user=user)
