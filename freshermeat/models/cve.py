from datetime import datetime

from freshermeat.bootstrap import db


class CVE(db.Model):
    """Represent a CVE."""

    id = db.Column(db.Integer, primary_key=True)
    cve_id = db.Column(db.String(), nullable=False)
    summary = db.Column(db.String(), default="")
    published_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # foreign keys
    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"), default=None)
