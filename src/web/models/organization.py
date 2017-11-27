
from web.models import Project
from bootstrap import db


class Organization(db.Model):
    """Represent an organization.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String())
    website = db.Column(db.String())

    # foreign keys
    icon_url = db.Column(db.String(), db.ForeignKey('icon.url'), default=None)

    # relationship
    projects = db.relationship(Project, backref='organization', lazy='dynamic',
                               cascade='all,delete-orphan')
