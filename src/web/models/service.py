
from sqlalchemy.dialects.postgresql import JSON

from bootstrap import db


class Service(db.Model):
    """Represent a service.
    """
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True)
    short_description = db.Column(db.String(300), unique=True)
    description = db.Column(db.String(), unique=True)
    website = db.Column(db.String())
    logo = db.Column(db.String())
    notification_email = db.Column(db.String(), default='')
    enabled = db.Column(db.Boolean(), default=True)

    required_informations = db.Column(JSON)

    def __repr__(self):
        return '<Name %r>' % (self.name)

    def __eq__(self, other):
        return self.name == other.name
