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
                                 paginate, token_required, user_only

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
    decorators = [
        user_only,
        token_required,
    ]

    @marshal_with(recipe_fields)
    def get(self, current_user, recipeid):
        """ Get a single recipe by ID."""
        abort_if_recipe_doesnt_exist(recipeid)
        recipe = RecipeModel.get_by_id(recipeid)
        return recipe

    def delete(self, current_user, recipeid):
        """ Delete a single recipe by ID."""
        abort_if_recipe_doesnt_exist(recipeid)
        recipe = RecipeModel.get_by_id(recipeid)
        RecipeModel.delete(recipe)
        return respond('Success', 201, 'Delete recipe success')

    @marshal_with(recipe_fields)
    def put(self, current_user, recipeid):
        """ Update a single recipe by ID."""
        abort_if_recipe_doesnt_exist(recipeid)
        args = parser.parse_args()
        recipetitle = args['recipetitle']
        recipedescription = args['recipedescription']
        recipe = RecipeModel.get_by_id(recipeid)
        update = RecipeModel.update(recipe, recipetitle, recipedescription)
        return update

# RecipeList
# shows a list of all RECIPES, and lets you POST to add new description
class RecipeList(Resource):
    """ Resource that returns a list of all recipes and adds a new Recipe."""
    decorators = [
        user_only,
        token_required,
    ]

    @marshal_with(recipe_collection_fields)
    @paginate()
    def get(self, current_user, category_id):
        """ Return all recipes"""
        category = None
        if category_id:
            category = CategoryModel.get_by_id(category_id)

        if not category:
            abort(404)

        RECIPES = RecipeModel.get_category_all(category.id)
        return RECIPES

    @marshal_with(recipe_fields)
    def post(self, current_user, category_id):
        """ Add a new Recipe"""
        args = parser.parse_args()
        recipetitle = args['recipetitle']
        recipedescription = args['recipedescription']
        category_id = args['category_id']
        newrecipe = RecipeModel(recipetitle=recipetitle, 
                               recipedescription=recipedescription, 
                               category_id=category_id).save()
        return newrecipe
