"""
    This is the Recipe resource file.
    Flask-RESTFUL is being used for all the REST operations
"""
from flask_restful import reqparse, abort, fields, marshal_with, Resource

# Models
from app.models import RecipeModel

# Fields
from app import meta_fields

# Helpers
from app.resources.helper import abort_if_recipe_doesnt_exist, respond, \
                                 paginate, token_required

recipe_fields = {
    'id': fields.Integer,
    'recipetitle': fields.String,
    'recipedescription': fields.String,
    'category_id': fields.Integer,
    'created_at' : fields.DateTime,
    'modified_at' : fields.DateTime
}

# Marshaled field definitions for collections of recipe objects
recipe_collection_fields = {
    'items': fields.List(fields.Nested(recipe_fields)),
    'meta': fields.Nested(meta_fields),
}

parser = reqparse.RequestParser()
parser.add_argument('recipetitle')
parser.add_argument('recipedescription')
parser.add_argument('category_id')

# Recipe
# shows a single Recipe item and lets you update or delete a Recipe item
class Recipe(Resource):
    """ Resource that gets, deletes and updates the Recipe item"""

    @token_required
    @marshal_with(recipe_fields)
    def get(self, current_user, recipeid):
        """ Get a single recipe by ID."""
        abort_if_recipe_doesnt_exist(recipeid)
        recipe = RecipeModel.get_by_id(recipeid)
        return recipe
    