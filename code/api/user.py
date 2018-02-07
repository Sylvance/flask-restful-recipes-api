#!/usr/bin/env python
import re
from flask import abort, g
from flask_restful import Resource, reqparse, marshal_with, fields

from code.api import api, meta_fields
from code.api.auth import self_only, token_required, ensure_auth_header
from code.models.user import User
from code.models.token import Token
from code.helpers import paginate, validate_json

def valid_str(value, name):
    if ' ' in value:
        raise ValueError("The parameter '{}' has spaces in: {}".format(name, value))
    if re.match(r'[A-Za-z]+$', value) is None:
        raise ValueError("Non-alphabetic characters for '{}' are not allowed in: {}".format(name, value))
    return value

def valid_id(value, name):
    if ' ' in value:
        raise ValueError("The parameter '{}' has spaces in: {}".format(name, value))
    if re.match(r'[0-9]+$', value) is None:
        raise ValueError("Non-integer characters for '{}' are not allowed in: {}".format(name, value))
    return value

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type = valid_str, \
                        help="Value not accepted for Username. String required.")
user_parser.add_argument('password', type = str, \
                        help="Password cannot be blank!")
user_parser.add_argument('email', type = str, \
                        help="Email cannot be blank!")
user_parser.add_argument('first_name', type = valid_str, \
                        help="Value not accepted for Firstname. String required.")
user_parser.add_argument('last_name', type = valid_str, \
                        help="Value not accepted for Lastname. String required.")

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
    """ Resource that gets, deletes and updates a user by id. """
    @ensure_auth_header
    @token_required
    @self_only
    @marshal_with(user_fields)
    def get(self, current_user, user_id=None, username=None):
        """ Resource that gets a user by id"""
        user = None
        print(user_id)
        if username is not None:
            user = User.get_by_username(username)
        else:
            user = User.get_by_id(user_id)

        if not user:
            abort(404, {"message" : "User does not exist"})

        return user

    @ensure_auth_header
    @token_required
    @self_only
    @validate_json
    @marshal_with(user_fields)
    def put(self, current_user, user_id=None, username=None):
        """ Resource that updates a user by id"""
        g.user.update(**user_parser.parse_args())
        return g.user

    @ensure_auth_header
    @token_required
    @self_only
    def delete(self, current_user, user_id=None, username=None):
        """ Resource that deletes a user by id"""
        g.user.delete()
        result = {
            'message': 'User has been deleted'
        }
        return result


class UserCollectionResource(Resource):
    """ Resource that gets a list of users and creates a new user """
    @marshal_with(user_collection_fields)
    @paginate()
    def get(self):
        """ Resource that gets a list of users"""
        users = User.query
        return users
    
    @validate_json
    def post(self):
        """ Resource that creates a new user """
        args = user_parser.parse_args()
        email = args['email']
        password = args['password']
        if not email:
            result = { 'message': 'Email cannot be blank' }
            return result, 400 
            
        if re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", email) and len(password) > 6:
            userbyemail = User.get_by_email(email)
            if not userbyemail:
                try:
                    user = User.create(**user_parser.parse_args())
                    if user:
                        result = { 'message': 'User has succesfully registered' }
                        return result, 201
                except Exception:
                    result = { 'message': 'Something went wrong when saving user'}
                    return result, 500
            else:
                result = { 'message': 'User already exists' }
                return result, 409
        result = { 'message': 'Incorrect credentials. Email should be correct. Password should be more than 6 characters' }
        return result, 400 


class UserSigninResource(Resource):
    """ Resource that signs in a user """
    @validate_json
    def post(self):
        """ Resource that signs in a user """
        args = user_parser.parse_args()
        email = args['email']
        username = args['username']
        password = args['password']
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) > 6:
            user = User.get_by_email(email)
            if user and user.check_password(password):
                token = user.encode_auth_token(user.id)
                result = { 'message': 'User has signed in.', 'token' : token.decode("utf-8") }
                return result, 200
            result = { 'message': 'User does not exist or incorrect password.' }
            return result, 400
        result = { 'message': 'Wrong email or password' }
        return result, 400


# SignoutUser
# Signs out a User if logged in
class UserSignoutResource(Resource):
    """ Resource that signs out a user """
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
                result = { 'message': 'Provide a valid authentication token' }
                return result, 403
            else:
                decoded_token_response = User.decode_auth_token(auth_token)
                if not isinstance(decoded_token_response, str):
                    token = Token(auth_token)
                    token.save()
                    result = { 'message': 'Successfully logged out' }
                    return result, 200
                result = { 'message': decoded_token_response }
                return result, 401
        result = { 'message': 'Provide an authorization header' }
        return result, 403

api.add_resource(UserResource, '/users/<int:user_id>', '/users/<username>')
api.add_resource(UserCollectionResource, '/users')
api.add_resource(UserSigninResource, '/users/signin')
api.add_resource(UserSignoutResource, '/users/signout')
