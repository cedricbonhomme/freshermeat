
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import JSON

from bootstrap import db


class Project(db.Model):
    """Represent a project.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    short_description = db.Column(db.String(300), unique=True)
    description = db.Column(db.String(), unique=True)
    website = db.Column(db.String())
    enabled = db.Column(db.Boolean(), default=True)
    last_updated = db.Column(db.DateTime(), default=datetime.utcnow())

    notification_email = db.Column(db.String(), default='')
    required_informations = db.Column(JSON)

    # foreign keys
    organization_id = db.Column(db.Integer(), db.ForeignKey('organization.id'))
    maintainer_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    icon_url = db.Column(db.String(), db.ForeignKey('icon.url'), default=None)

    # relationships
    tag_objs = db.relationship('Tag', back_populates='project',
                                cascade='all,delete-orphan',
                                lazy=False,
                                foreign_keys='[Tag.project_id]')
    tags = association_proxy('tag_objs', 'text')


    def __repr__(self):
        return '<Name %r>' % (self.name)
