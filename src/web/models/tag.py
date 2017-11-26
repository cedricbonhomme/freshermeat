#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bootstrap import db


class Tag(db.Model):
    text = db.Column(db.String, primary_key=True, unique=False)

    # foreign keys
    project_id = db.Column(db.Integer,
                           db.ForeignKey('project.id', ondelete='CASCADE'),
                           primary_key=True)

    # relationships
    article = db.relationship('Project', back_populates='tag_objs',
                                                    foreign_keys=[project_id])

    def __init__(self, text):
        self.text = text
