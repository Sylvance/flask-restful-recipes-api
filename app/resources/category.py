"""
    This is the Category resource file.
    Flask-RESTFUL is being used for all the REST operations
"""
from flask_restful import reqparse, abort, fields, marshal_with, Resource

# Models
from app.models import CategoryModel

# Fields
from app import meta_fields

# Helpers
from app.resources.helper import abort_if_category_doesnt_exist, respond, \
                                paginate, token_required

category_fields = {
    'id': fields.Integer,
    'categorytitle': fields.String,
    'categorydescription' : fields.String,
    'user_id' : fields.Integer,
    'created_at' : fields.DateTime,
    'modified_at' : fields.DateTime
}

# Marshaled field definitions for collections of category objects
category_collection_fields = {
    'items': fields.List(fields.Nested(category_fields)),
    'meta': fields.Nested(meta_fields),
}

parser = reqparse.RequestParser()
parser.add_argument('categorytitle')
parser.add_argument('categorydescription')
parser.add_argument('user_id')

# Category
# shows a single Category item and lets you update or delete a Category item
class Category(Resource):
    """ Resource that gets, deletes and updates categories. """

    @token_required
    @marshal_with(category_fields)
    def get(self, current_user, categoryid):
        """ Get a single category by ID."""
        abort_if_category_doesnt_exist(categoryid)
        category = CategoryModel.get_by_id(categoryid)
        return category

    @token_required
    def delete(self, current_user, categoryid):
        """ Delete a single category by ID."""
        abort_if_category_doesnt_exist(categoryid)
        category = CategoryModel.get_by_id(categoryid)
        CategoryModel.delete(category)
        return respond('Success', 201, 'Delete category success')

    @token_required
    @marshal_with(category_fields)
    def put(self, current_user, categoryid):
        """ Update a single category by ID."""
        abort_if_category_doesnt_exist(categoryid)
        args = parser.parse_args()
        categorytitle = args['categorytitle']
        categorydescription = args['categorydescription']
        category = CategoryModel.get_by_id(categoryid)
        update = CategoryModel.update(category, categorytitle, categorydescription)
        return update


# CategoryList
# shows a list of all CATEGORIES, and lets you POST to add new description
class CategoryList(Resource):
    """ Resource that returns a list of all Categories and adds a new Category."""

    @token_required
    @marshal_with(category_collection_fields)
    @paginate()
    def get(self, current_user):
        """ Return all Categories"""
        CATEGORIES = CategoryModel.get_all()
        return CATEGORIES
