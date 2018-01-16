#!/usr/bin/env python
import re
from flask import abort, g
from flask_restful import Resource, reqparse, marshal_with, fields

from code.api import api, meta_fields
from code.api.auth import self_only, token_required
from code.models.user import User
from code.models.token import Token
from code.helpers import paginate

user_parser = reqparse.RequestParser()
user_parser.add_argument('username')
user_parser.add_argument('password')
user_parser.add_argument('email')
user_parser.add_argument('first_name')
user_parser.add_argument('last_name')

# From the request headers
parser = reqparse.RequestParser()
parser.add_argument('Authorization', location='headers')


# Marshaled field definitions for user objects
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
}

user_public_fields = {
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
}

# Marshaled field definitions for collections of user objects
user_collection_fields = {
    'items': fields.List(fields.Nested(user_public_fields)),
    'meta': fields.Nested(meta_fields),
}


class UserResource(Resource):
    @token_required
    @self_only
    @marshal_with(user_fields)
    def get(self, current_user, user_id=None, username=None):
        user = None
        print(user_id)
        if username is not None:
            user = User.get_by_username(username)
        else:
            user = User.get_by_id(user_id)

        if not user:
            abort(404)

        return user

    @token_required
    @self_only
    @marshal_with(user_fields)
    def post(self, current_user, user_id=None, username=None):
        g.user.update(**user_parser.parse_args())
        return g.user

    @token_required
    @self_only
    def delete(self, current_user, user_id=None, username=None):
        g.user.delete()
        result = {
            'status': 'Success',
            'status code': 204,
            'message': 'User has been deleted'
        }
        return result, 204


class UserCollectionResource(Resource):
    @marshal_with(user_collection_fields)
    @paginate()
    def get(self):
        users = User.query
        return users

    def post(self):
        args = user_parser.parse_args()
        email = args['email']
        username = args['username']
        password = args['password']
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) > 6:
            userbyemail = User.get_by_email(email)
            # userbyname = User.get_by_username(username)
            if not userbyemail:
                try:
                    user = User.create(**user_parser.parse_args())
                    if user:
                        result = {
                            'status': 'Success',
                            'status code': 201,
                            'message': 'User has succesfully registered'
                        }
                        return result, 201
                except:
                    result = {
                        'status': 'Fail',
                        'status code': 500,
                        'message': 'Something went wrong when saving user'
                    }
                    return result, 500
            else:
                result = {
                    'status': 'Fail',
                    'status code': 409,
                    'message': 'User already exists'
                }
                return result, 409
        result = {
            'status': 'Fail',
            'status code': 403,
            'message': 'Wrong email or password'
        }
        return result, 403 


class UserSigninResource(Resource):

    def post(self):
        args = user_parser.parse_args()
        email = args['email']
        username = args['username']
        password = args['password']
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) > 6:
            user = User.get_by_email(email)
            if user and user.check_password(password):
                token = user.encode_auth_token(user.id)
                result = {
                    'status': 'Success',
                    'status code': 200,
                    'message': 'User has signed in.',
                    'token' : token.decode("utf-8")
                }
                return result, 200
            result = {
                'status': 'Fail',
                'status code': 401,
                'message': 'User does not exist or incorrect password.'
            }
            return result, 401
        result = {
            'status': 'Fail',
            'status code': 401,
            'message': 'Wrong email or password'
        }
        return result, 401


# SignoutUser
# Signs out a User if logged in
class UserSignoutResource(Resource):
    """ Signout class"""

    def get(self):
        """
        Try to logout a user using a token
        :return:
        """
        args = parser.parse_args()
        auth_header = args['Authorization']
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                result = {
                    'status': 'Fail',
                    'status code': 403,
                    'message': 'Provide a valid authentication token'
                }
                return result, 403
            else:
                decoded_token_response = User.decode_auth_token(auth_token)
                if not isinstance(decoded_token_response, str):
                    token = Token(auth_token)
                    token.save()
                    result = {
                        'status': 'Success',
                        'status code': 200,
                        'message': 'Successfully logged out'
                    }
                    return result, 200
                result = {
                    'status': 'Fail',
                    'status code': 401,
                    'message': decoded_token_response
                }
                return result, 401
        result = {
            'status': 'Fail',
            'status code': 403,
            'message': 'Provide an authorization header'
        }
        return result, 403

api.add_resource(UserResource, '/users/<int:user_id>', '/users/<username>')
api.add_resource(UserCollectionResource, '/users')
api.add_resource(UserSigninResource, '/users/signin')
api.add_resource(UserSignoutResource, '/users/signout')