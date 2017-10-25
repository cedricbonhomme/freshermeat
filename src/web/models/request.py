
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import JSON
from validate_email import validate_email

from bootstrap import db


class Request(db.Model, UserMixin):
    """Represent a request.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)

    checked = db.Column(db.Boolean(), default=False)
    notification_sent = db.Column(db.Boolean(), default=False)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    required_informations = db.Column(JSON)

    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))

    # Relationship
    service = db.relationship('Service', backref="requests")

    @validates('email')
    def validates_email(self, key, value):
        assert len(value) <= 100, 'email too long'
        assert validate_email(value), 'email not valid'
        return str(value).strip()

    @validates('firstname')
    def validates_firstname(self, key, value):
        assert len(value) <= 100, 'firstname too long'
        return str(value).strip()

    @validates('lastname')
    def validates_lastname(self, key, value):
        assert len(value) <= 100, 'lastname too long'
        return str(value).strip()
