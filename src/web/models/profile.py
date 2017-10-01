
from datetime import datetime
from flask_login import UserMixin
from werkzeug import check_password_hash

from bootstrap import db

class Profile(db.Model, UserMixin):
    """
    Represent a user.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    firstname = db.Column(db.String(), default='')
    lastname = db.Column(db.String(), default='')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    services = db.relationship("Service", backref="service")
