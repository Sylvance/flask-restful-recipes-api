#!/usr/bin/env python

from flask import abort, g
from flask_restful import Resource, reqparse, marshal_with, fields

from code.api import api, meta_fields
from code.api.auth import self_only, token_required
from code.models.recipe import Recipe
from code.models.category import Category
from code.helpers import paginate

recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument('title', type=str)
recipe_parser.add_argument('description', type=str)
recipe_parser.add_argument('category_id', type=int)

recipe_collection_parser = reqparse.RequestParser()
recipe_collection_parser.add_argument('title', type=str)


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

    @token_required
    @self_only
    @marshal_with(recipe_fields)
    def get(self, current_user, recipe_id=0, **kwargs):
        recipe = Recipe.get_by_id(recipe_id)

        if not recipe:
            abort(404)

        return recipe

    @token_required
    @self_only
    @marshal_with(recipe_fields)
    def post(self, current_user, recipe_id=0, **kwargs):
        recipe = Recipe.get_by_id(recipe_id)

        if not recipe:
            abort(404)

        recipe.update(**recipe_parser.parse_args())
        return recipe

    @token_required
    @self_only
    def delete(self, current_user, recipe_id=0, **kwargs):
        recipe = Recipe.get_by_id(recipe_id)

        if not recipe:
            abort(404)

        recipe.delete()
        return {}, 204


class RecipeCollectionResource(Resource):

    @token_required
    @self_only
    @marshal_with(recipe_collection_fields)
    @paginate()
    def get(self, current_user, category_id=None, title=None):
        # Find category that recipe goes with
        category = None
        if category_id:
            category = Category.get_by_id(category_id)
        else:
            category = Category.get_by_title(title)

        if not category:
            abort(404)

        # Get the category's recipes
        recipes = Recipe.query.filter_by(category_id=category.id)

        args = recipe_collection_parser.parse_args()
        # fancy url argument query filtering!
        if args['title'] is not None:
            recipes.filter_by(title=args['title'])

        return recipes

    @token_required
    @self_only
    @marshal_with(recipe_fields)
    def post(self, current_user, category_id=None, title=None):
        args = recipe_parser.parse_args()
        recipe = Recipe.create(**args)
        return recipe, 201


api.add_resource(RecipeResource, '/categories/<int:category_id>/recipes/<int:recipe_id>',
                 '/categories/<title>/recipes/<int:recipe_id>')
api.add_resource(RecipeCollectionResource, '/categories/<int:category_id>/recipes',
                 '/categories/<title>/recipes')