
from bootstrap import db


class CVE(db.Model):
    """Represent a CVE.
    """
    id = db.Column(db.Integer, primary_key=True)
    cve_id = db.Column(db.String(), nullable=False)
    summary = db.Column(db.String(), default='')

    # foreign keys
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'),
                           default=None)
