
from datetime import datetime
from sqlalchemy.orm import validates

from web.models import Project
from bootstrap import db


class Organization(db.Model):
    """Represent an organization.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(), default='')
    short_description = db.Column(db.String(400))
    organization_type = db.Column(db.String(100), default='')
    website = db.Column(db.String(), default='')
    last_updated = db.Column(db.DateTime(), default=datetime.utcnow())

    cve_vendor = db.Column(db.String(), default='')

    # foreign keys
    icon_url = db.Column(db.String(), db.ForeignKey('icon.url'), default=None)

    # relationship
    projects = db.relationship(Project, backref='organization', lazy='dynamic',
                               cascade='all,delete-orphan')

    @validates('name')
    def validates_name(self, key, value):
        assert len(value) <= 100, \
            AssertionError("maximum length for name: 100")
        return value.replace(' ', '').strip()
