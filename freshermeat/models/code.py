from datetime import datetime
from freshermeat.bootstrap import db


class Code(db.Model):
    """Represent a source code (a repository)."""

    id = db.Column(db.Integer(), primary_key=True)
    repository_url = db.Column(db.String(), nullable=False)
    scm_type = db.Column(db.String(), nullable=False, default="Git")
    last_updated = db.Column(db.DateTime(), default=datetime.utcnow())

    # foreign keys
    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"), default=None)
