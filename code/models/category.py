#!/usr/bin/env python

import datetime

from code.database import (
    db,
    Model,
    SurrogatePK,
    relationship,
    ReferenceCol,
)

from .recipe import Recipe


class Category(SurrogatePK, Model):
    __tablename__ = 'categories'
    # Define a foreign key relationship to a User object
    user_id = ReferenceCol('users')
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(256), nullable=False)
    modified_at = db.Column(db.DateTime(256), nullable=False)

    recipes = relationship(Recipe, cascade="all, delete-orphan", backref=db.backref('category'))

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    @classmethod
    def get_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def get_user_all(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    def __repr__(self):  # pragma: nocover
        return '<Category({title!r})>'.format(title=self.title)
