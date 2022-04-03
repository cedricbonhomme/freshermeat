#! /usr/bin/env python
from freshermeat.bootstrap import db


class Tag(db.Model):
    text = db.Column(db.String(), primary_key=True, unique=False)

    # foreign keys
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"), primary_key=True
    )

    # relationships
    project = db.relationship(
        "Project", back_populates="tag_objs", foreign_keys=[project_id]
    )

    def __init__(self, text, project_id):
        self.text = text
        self.project_id = project_id

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text
