#!/usr/bin/env python
import re
from flask import abort, g
from flask_restful import Resource, reqparse, marshal_with, fields

from code.api import api, meta_fields
from code.api.auth import self_only, token_required, ensure_auth_header
from code.models.recipe import Recipe
from code.models.category import Category
from code.helpers import paginate, abort_if_exists, validate_json

def valid_str(value, name):
    if ' ' in value:
        raise ValueError("The parameter '{}' has spaces in: {}".format(name, value))
    if re.match(r'[A-Za-z]+$', value) is None:
        raise ValueError("Non-alphabetic characters for '{}' are not allowed in: {}".format(name, value))
    return value

recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument('title', type=valid_str)
recipe_parser.add_argument('description', type=valid_str)
recipe_parser.add_argument('category_id', type=int)

recipe_collection_parser = reqparse.RequestParser()
recipe_collection_parser.add_argument('title', type=valid_str)


# Marshaled field definitions for recipe objects
recipe_fields = {
    'id': fields.Integer,
    'category_id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'created_at' : fields.DateTime,
    'modified_at' : fields.DateTime
}

# Marshaled field definitions for collections of recipe objects
recipe_collection_fields = {
    'items': fields.List(fields.Nested(recipe_fields)),
    'meta': fields.Nested(meta_fields),
}


class RecipeResource(Resource):
    """ Resource that gets, deletes and updates a recipe by id """
    @ensure_auth_header
    @token_required
    @self_only
    @marshal_with(recipe_fields)
    def get(self, current_user, category_id=None, recipe_id=0, **kwargs):
        """ Resource that gets a recipe by id """
        recipe = Recipe.get_by_id(recipe_id)

        if not recipe:
            abort(404, { "message" : "Recipe does not exist." })

        return recipe

    @ensure_auth_header
    @token_required
    @self_only
    @validate_json
    @marshal_with(recipe_fields)
    def put(self, current_user, category_id=None, recipe_id=0, **kwargs):
        """ Resource that updates a recipe by id """
        args = recipe_parser.parse_args()
        recipe = Recipe.get_by_id(recipe_id)
        if args['category_id'] != category_id:
            abort(404, { "message" : "Provide valid category id." })
        # abort if recipe exists
        abort_if_exists(g.user.id, category_id=category_id, recipe_name=args['title'])

        if not recipe:
            abort(404, { "message" : "Recipe does not exist." })

        recipe.update(**recipe_parser.parse_args())
        return recipe

    @ensure_auth_header
    @token_required
    @self_only
    def delete(self, current_user, category_id=None, recipe_id=0, **kwargs):
        """ Resource that deletes a recipe by id """
        recipe = Recipe.get_by_id(recipe_id)

        if not recipe:
            abort(404)

        recipe.delete()
        result = {
            'status': 'Deleted',
            'status code': 204,
            'message': 'Recipe deleted successfully'
        }
        return result


class RecipeCollectionResource(Resource):
    """ Resource that gets a list of recipes and creates a new recipe """
    @ensure_auth_header
    @token_required
    @self_only
    @marshal_with(recipe_collection_fields)
    @paginate()
    def get(self, current_user, category_id=None, title=None):
        """ Resource that gets a list of recipes """        
        # Find category that recipe goes with
        category = None
        if category_id:
            category = Category.get_by_id(category_id)
        else:
            category = Category.get_by_title(title)

        if not category:
            abort(404, { "message" : "Category does not exist." })

        # Get the category's recipes
        recipes = Recipe.query.filter_by(category_id=category.id)

        args = recipe_collection_parser.parse_args()
        # fancy url argument query filtering!
        if args['title'] is not None:
            recipes = Recipe.query.filter(Recipe.title.ilike(
                '%' + args['title'] + '%')).filter(Recipe.category_id == category.id)
            if not recipes:
                abort(404, { "message": "Recipes for query do not exist" })

        return recipes

    @ensure_auth_header
    @token_required
    @self_only
    @validate_json
    @marshal_with(recipe_fields)
    def post(self, current_user, category_id=None, title=None):
        """ Resource that creates a new recipe """        
        args = recipe_parser.parse_args()
        if args['category_id'] != category_id:
            abort(404, { "message" : "Provide valid category id." })
            
        category = Category.get_by_id(category_id)
        if not category:
            abort(404, { "message" : "Category does not exist." })
        # abort if recipe exists
        abort_if_exists(g.user.id, category_id=category_id, recipe_name=args['title'])
        recipe = Recipe.create(**args)
        return recipe, 201


api.add_resource(RecipeResource, '/categories/<int:category_id>/recipes/<int:recipe_id>',
                 '/categories/<title>/recipes/<int:recipe_id>')
api.add_resource(RecipeCollectionResource, '/categories/<int:category_id>/recipes',
                 '/categories/<title>/recipes')
