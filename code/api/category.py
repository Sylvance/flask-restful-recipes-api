#!/usr/bin/env python

from flask import abort, g
from flask_restful import Resource, reqparse, marshal_with, fields

from code.api import api, meta_fields
from code.api.auth import self_only, token_required
from code.models.category import Category
from code.models.user import User
from code.helpers import paginate

category_parser = reqparse.RequestParser()
category_parser.add_argument('title', type=str)
category_parser.add_argument('description', type=str)

category_collection_parser = reqparse.RequestParser()
category_collection_parser.add_argument('title', type=str)


# Marshaled field definitions for category objects
category_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'created_at' : fields.DateTime,
    'modified_at' : fields.DateTime
}

# Marshaled field definitions for collections of category objects
category_collection_fields = {
    'items': fields.List(fields.Nested(category_fields)),
    'meta': fields.Nested(meta_fields),
}


class CategoryResource(Resource):

    @token_required
    @self_only
    @marshal_with(category_fields)
    def get(self, current_user, user_id=None, category_id=0, **kwargs):
        category = Category.get_by_id(category_id)

        if not category:
            abort(404)

        return category

    @token_required
    @self_only
    @marshal_with(category_fields)
    def post(self, current_user, user_id=None, category_id=0, **kwargs):
        category = Category.get_by_id(category_id)

        if not category:
            abort(404)

        category.update(**category_parser.parse_args())
        return category

    @token_required
    @self_only
    def delete(self, current_user, user_id=None, category_id=0, **kwargs):
        category = Category.get_by_id(category_id)

        if not category:
            abort(404)

        category.delete()
        return {}, 204


class CategoryCollectionResource(Resource):

    @token_required
    @self_only
    @marshal_with(category_collection_fields)
    @paginate()
    def get(self, current_user, user_id=None, username=None):
        # Find user that category goes with
        user = None
        if user_id:
            user = User.get_by_id(user_id)
        else:
            user = User.get_by_username(username)

        if not user:
            abort(404)

        # Get the user's categories
        categories = Category.query.filter_by(user_id=user.id)

        args = category_collection_parser.parse_args()
        # fancy url argument query filtering!
        if args['title'] is not None:
            categories.filter_by(title=args['title'])

        return categories

    @token_required
    @self_only
    @marshal_with(category_fields)
    def post(self, current_user, user_id=None, username=None):
        args = category_parser.parse_args()
        # user owns the category
        args['user_id'] = g.user.id
        category = Category.create(**args)
        return category, 201


api.add_resource(CategoryResource, '/users/<int:user_id>/categories/<int:category_id>',
                 '/users/<username>/categories/<int:category_id>')
api.add_resource(CategoryCollectionResource, '/users/<int:user_id>/categories',
                 '/users/<username>/categories')