#!/usr/bin/env python
import re
from flask import abort, g
from flask_restful import Resource, reqparse, marshal_with, fields

from code.api import api, meta_fields
from code.api.auth import self_only, token_required, ensure_auth_header
from code.models.category import Category
from code.models.user import User
from code.helpers import paginate, abort_if_exists, validate_json

def valid_str(value, name):
    if ' ' in value:
        raise ValueError("The parameter '{}' has spaces in: {}".format(name, value))
    if re.match(r'[A-Za-z]+$', value) is None:
        raise ValueError("Non-alphabetic characters for '{}' are not allowed in: {}".format(name, value))
    return value

category_parser = reqparse.RequestParser()
category_parser.add_argument('title', type=valid_str)
category_parser.add_argument('description', type=str)
category_collection_parser = reqparse.RequestParser()
category_collection_parser.add_argument('title', type=valid_str)


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
    """ Resource that gets, deletes and updates a category by id"""
    @ensure_auth_header
    @token_required
    @self_only
    @marshal_with(category_fields)
    def get(self, current_user, user_id=None, category_id=0, **kwargs):
        """ Resource that gets a category by id"""
        category = Category.get_by_id(category_id)
        if not category:
            abort(404, { "message": "Category does not exist" })
        return category

    @ensure_auth_header
    @token_required
    @self_only
    @validate_json
    @marshal_with(category_fields)
    def put(self, current_user, user_id=None, category_id=0, **kwargs):
        """ Resource that updates a category by id"""
        category = Category.get_by_id(category_id)
        args = category_parser.parse_args()
        abort_if_exists(g.user.id, category_name=args['title'])

        if not category:
            abort(404, { "message": "Category does not exist" })

        category.update(**category_parser.parse_args())
        return category

    @ensure_auth_header
    @token_required
    @self_only
    def delete(self, current_user, user_id=None, category_id=0, **kwargs):
        """ Resource that deletes a category by id"""
        category = Category.get_by_id(category_id)

        if not category:
            abort(404)

        category.delete()
        result = {
            'status': 'Deleted',
            'message': 'Category deleted successfully'
        }
        return result


class CategoryCollectionResource(Resource):
    """ Resource that gets a list of categories and creates a new category """
    @ensure_auth_header
    @token_required
    @self_only
    @marshal_with(category_collection_fields)
    @paginate()
    def get(self, current_user, user_id=None, username=None, title=None):
        """ Resource that gets a list of categories """
        # Find user that category goes with
        user = None
        if user_id:
            user = User.get_by_id(user_id)
        else:
            user = User.get_by_username(username)

        if not user:
            abort(404, { "message": "User does not exist" })

        # Get the user's categories
        categories = Category.query.filter_by(user_id=user.id)

        args = category_collection_parser.parse_args()
        # fancy url argument query filtering!
        if args['title'] is not None:
            categories = Category.query.filter(Category.title.ilike(
                '%' + args['title'] + '%')).filter(Category.user_id == g.user.id)
            if not categories:
                abort(404, { "message": "Categories for query do not exist" })

        return categories

    @ensure_auth_header
    @token_required
    @self_only
    @validate_json
    @marshal_with(category_fields)
    def post(self, current_user, user_id=None, username=None):
        """ Resource that creates a new category """
        args = category_parser.parse_args()
        abort_if_exists(g.user.id, category_name=args['title'])
        # user owns the category
        args['user_id'] = g.user.id
        category = Category.create(**args)
        return category, 201


api.add_resource(CategoryResource, '/users/<int:user_id>/categories/<int:category_id>',
                 '/users/<username>/categories/<int:category_id>')
api.add_resource(CategoryCollectionResource, '/users/<int:user_id>/categories',
                 '/users/<username>/categories')
