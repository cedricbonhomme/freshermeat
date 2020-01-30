#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Index
from freshermeat.bootstrap import db


class News(db.Model):
    "Represent an article from a feed."
    id = db.Column(db.Integer(), primary_key=True)
    entry_id = db.Column(db.String(), nullable=False)
    link = db.Column(db.String())
    title = db.Column(db.String())
    content = db.Column(db.String())
    published = db.Column(db.DateTime(), default=datetime.utcnow)
    retrieved_date = db.Column(db.DateTime(), default=datetime.utcnow)

    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'))
    feed_id = db.Column(db.Integer(), db.ForeignKey('feed.id'))

    # index
    idx_article_pid = Index('project_id')
    idx_article_pid_fid = Index('project_id', 'feed_id')


    def __repr__(self):
        return "<News(id=%d, entry_id=%s, title=%r, " \
               "date=%r, retrieved_date=%r)>" % (self.id, self.entry_id,
                       self.title, self.published, self.retrieved_date)
