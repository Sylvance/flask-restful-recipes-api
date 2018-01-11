"""
    This is the Category resource file.
    Flask-RESTFUL is being used for all the REST operations
"""
from flask_restful import reqparse, abort, fields, marshal_with, Resource

# Models
from app.models import UserModel, CategoryModel

# Fields
from app import meta_fields

# Helpers
from app.resources.helper import abort_if_category_doesnt_exist, respond, \
                                paginate, token_required, user_only

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
    decorators = [
        user_only,
        token_required,
    ]

    @marshal_with(category_fields)
    def get(self, current_user, categoryid):
        """ Get a single category by ID."""
        abort_if_category_doesnt_exist(categoryid)
        category = CategoryModel.get_by_id(categoryid)
        return category

    def delete(self, current_user, categoryid):
        """ Delete a single category by ID."""
        abort_if_category_doesnt_exist(categoryid)
        category = CategoryModel.get_by_id(categoryid)
        CategoryModel.delete(category)
        return respond('Success', 201, 'Delete category success')

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
    decorators = [
        user_only,
        token_required,
    ]

    @marshal_with(category_collection_fields)
    @paginate()
    def get(self, current_user, user_id):
        """ Return all Categories"""
        user = None
        if user_id:
            user = UserModel.get_by_id(user_id)

        if not user:
            abort(404)

        CATEGORIES = CategoryModel.get_user_all(user.id)
        return CATEGORIES

    @marshal_with(category_fields)
    def post(self, current_user, user_id):
        """ Add a new Category"""
        args = parser.parse_args()
        categorytitle = args['categorytitle']
        categorydescription = args['categorydescription']
        user_id = args['user_id']
        category = CategoryModel.get_by_title(categorytitle)
        if not category:
            newcategory = CategoryModel(categorytitle=categorytitle, 
                                       categorydescription=categorydescription, 
                                       user_id=user_id).save()
            return newcategory
        else:
            return respond('Fail', 409, 'Category already exists')
