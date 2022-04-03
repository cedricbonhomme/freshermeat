#! /usr/bin/python
from werkzeug.security import generate_password_hash

from freshermeat.bootstrap import db
from freshermeat.models import User


def create_user(login, password, is_admin):
    user = User(
        login=login,
        pwdhash=generate_password_hash(password),
        is_active=True,
        is_admin=is_admin,
    )
    db.session.add(user)
    db.session.commit()
