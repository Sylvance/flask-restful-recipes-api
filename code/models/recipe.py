#!/usr/bin/env python

import datetime

from code.database import (
    db,
    Model,
    SurrogatePK,
    ReferenceCol,
)


class Recipe(SurrogatePK, Model):
    __tablename__ = 'recipes'
    # Define a foreign key relationship to a Category object
    category_id = ReferenceCol('categories')
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
    
    @classmethod
    def get_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def get_category_all(cls, category_id):
        return cls.query.filter_by(category_id=category_id)

    @classmethod
    def recipe_exists(cls, category_id, title):
        recipes = cls.query.filter_by(category_id=category_id)
        recipeslist = []
        for recipe in recipes:
            recipeslist.append(recipe.title)
        if title in recipeslist:
            return True
        else:
            return False 
