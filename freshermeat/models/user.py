import re
import secrets
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash

from freshermeat.bootstrap import db
from freshermeat.models import Project


class User(db.Model, UserMixin):
    """
    Represent a user.
    """

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), unique=True, nullable=False)
    pwdhash = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow())
    apikey = db.Column(db.String(), default=secrets.token_urlsafe(50))

    public_profile = db.Column(db.Boolean(), default=True)

    # user rights
    is_active = db.Column(db.Boolean(), default=False)
    is_admin = db.Column(db.Boolean(), default=False)
    is_api = db.Column(db.Boolean(), default=False)

    # relationship
    positions = db.relationship(
        "Project", backref="manager", lazy="dynamic", foreign_keys=[Project.manager_id]
    )
    contributions = db.relationship(
        "Project",
        backref="submitter",
        lazy="dynamic",
        foreign_keys=[Project.submitter_id],
    )

    def __repr__(self):
        return self.login

    def get_id(self):
        """
        Return the id of the user.
        """
        return self.id

    def generate_apikey(self):
        self.apikey = secrets.token_urlsafe(50)

    def check_password(self, password):
        """
        Check the password of the user.
        """
        return check_password_hash(self.pwdhash, password)

    @validates("login")
    def validates_login(self, key, value):
        assert 3 <= len(value) <= 30, AssertionError("maximum length for login: 30")
        return re.sub(r"[^a-zA-Z0-9_\.]", "", value.strip())
