from datetime import datetime

from freshermeat.bootstrap import db

association_table_license = db.Table(
    "association_submissions_licenses",
    db.metadata,
    db.Column("submission_id", db.Integer, db.ForeignKey("submission.id")),
    db.Column("license_id", db.Integer, db.ForeignKey("license.id")),
)


class Submission(db.Model):
    """Represent a submission.
    """

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), unique=True)
    project_description = db.Column(db.String())
    project_website = db.Column(db.String())
    reviewed = db.Column(db.Boolean(), default=False)
    accepted = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # relationships
    licenses = db.relationship(
        "License", secondary=lambda: association_table_license, backref="submissions"
    )
