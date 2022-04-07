from datetime import datetime

from freshermeat.bootstrap import db


class Language(db.Model):
    """Represent a language."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), default="", nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

    def __str__(self):
        return self.name
