
from datetime import datetime
from bootstrap import db


class Release(db.Model):
    """Represent a release.
    """
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(), default='', nullable=False)
    state = db.Column(db.String(), default='')  #ie: stable
    scope = db.Column(db.String(), default='')  #ie: minor bugfix feature
    changes = db.Column(db.String(), default='')
    download = db.Column(db.String(), default='')
    published_at = db.Column(db.DateTime(), default=datetime.utcnow())

    # foreign keys
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'),
                           default=None)
