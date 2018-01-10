"""
    This is the User resource file.
    Flask-RESTFUL is being used for all the REST operations
"""
import re
from flask import jsonify
from flask_restful import reqparse, fields, marshal_with, Resource

# Models
from app.models import UserModel, BannedToken

# Encryption
from app import bcrypto

# Fields
from app import meta_fields

# Helpers
from app.resources.helper import abort_if_user_doesnt_exist, respond, \
                                token_required, paginate

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email' : fields.String,
    'bio' : fields.String,
    'created_at' : fields.DateTime,
    'modified_at' : fields.DateTime
}

# Marshaled field definitions for collections of user objects
user_collection_fields = {
    'items': fields.List(fields.Nested(user_fields)),
    'meta': fields.Nested(meta_fields),
}

# From the request json
parser = reqparse.RequestParser()
parser.add_argument('bio')
parser.add_argument('email')
parser.add_argument('username')
parser.add_argument('password')
# From the request headers
parser.add_argument('Authorization', location='headers')

# User
# shows a single User item and lets you update or delete a User item

class User(Resource):
    """ Resource that gets, deletes and updates the User item"""

    @token_required
    @marshal_with(user_fields)
    def get(self, current_user, userid):
        """ Get a single user by ID."""
        abort_if_user_doesnt_exist(userid)
        user = UserModel.get_by_id(userid)
        return user

    @token_required
    def delete(self, current_user, userid):
        """ Delete a single user by ID."""
        abort_if_user_doesnt_exist(userid)
        user = UserModel.get_by_id(userid)
        UserModel.delete(user)
        return respond('Success', 201, 'Delete user success')

# SignupUser
# Signs up a User if not exist
class SignupUser(Resource):
    """ Signup class"""
    
    def post(self):
        """ Add a new User"""
        args = parser.parse_args()
        bio = args['bio']
        email = args['email']
        username = args['username']
        password = args['password']
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) > 6:
            user = UserModel.get_by_email(email)
            if not user:
                token = UserModel(username=username, 
                                    email=email,
                                    bio=bio, 
                                    password=password).save()
                result = respond('Success', 
                                  200, 
                                  'Successfully signed up', 
                                  token.decode("utf-8"))
                return result
            else:
                result = {
                    'status': 'Fail',
                    'status code': 409,
                    'message': 'User already exists'
                }
                return result
        result = {
            'status': 'Fail',
            'status code': 403,
            'message': 'Wrong email or password'
        }
        return result
