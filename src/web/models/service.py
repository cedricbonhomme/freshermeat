
from sqlalchemy.dialects.postgresql import JSON

from bootstrap import db

class Service(db.Model):
    """Represent a service.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    short_description = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(), unique=True)
    webpage = db.Column(db.String())
    logo = db.Column(db.String())

    required_informations = db.Column(db.JSON)

    def __repr__(self):
        return '<Name %r>' % (self.name)

    def __eq__(self, other):
        return self.name == other.name
