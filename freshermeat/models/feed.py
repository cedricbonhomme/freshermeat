#! /usr/bin/env python
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy import Index

from freshermeat.bootstrap import db
from freshermeat.models.news import News


class Feed(db.Model):
    """
    Represent a feed.
    """

    id = db.Column(db.Integer(), primary_key=True)
    link = db.Column(db.String(), nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    # relationship
    news = db.relationship(
        News,
        backref="source",
        lazy="dynamic",
        cascade="all,delete-orphan",
        order_by=desc(News.published),
    )

    # index
    idx_feed_pid = Index("project_id")

    def __repr__(self):
        return "<Feed %r>" % (self.link)
