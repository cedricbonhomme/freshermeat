
from web.models import Project
from bootstrap import db


class Organization(db.Model):
    """Represent an organization.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(), unique=True)
    website = db.Column(db.String())

    # relationship
    icon_url = db.Column(db.String(), db.ForeignKey('icon.url'), default=None)
    projects = db.relationship(Project, backref='organization', lazy='dynamic',
                               cascade='all,delete-orphan')
