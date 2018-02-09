
from sqlalchemy.dialects.postgresql import JSON

from datetime import datetime
from bootstrap import db


class Service(db.Model):
    """Represent a service.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    service_enabled = db.Column(db.Boolean(), default=True)
    notification_email = db.Column(db.String(), default='')
    required_informations = db.Column(JSON, default=None)

    # foreign keys
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'),
                           default=None)
