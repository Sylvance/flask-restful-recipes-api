#!/usr/bin/env python

import functools
from functools import wraps
from flask import g, abort, request, make_response, jsonify
from code.models.user import User
from code.models.category import Category
from code.models.recipe import Recipe

def self_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get('username', None):
            if g.user.username != kwargs['username']:
                abort(403, {"status" : "Access denied","state" : "Entity not accessible to current user. Provide valid name or id."})
        if kwargs.get('user_id', None):
            if g.user.id != kwargs['user_id']:
                abort(403, {"status" : "Access denied","state" : "Entity not accessible to current user. Provide valid name or id."})
        if kwargs.get('category_id', None):
            category = Category.get_by_id(kwargs['category_id'])
            if not category:
                abort(404, {"status" : "Bad request","state" : "Category does not exist"})
            if g.user.id != category.user_id:
                abort(403, {"status" : "Access denied","state" : "Entity not accessible to current user. Provide valid name or id."})
        if kwargs.get('recipe_id', None):
            recipe = Recipe.get_by_id(kwargs['recipe_id'])
            category = Category.get_by_id(recipe.category_id)
            if not recipe:
                abort(404, {"status" : "Bad request","state" : "Recipe does not exist"})
            if g.user.id != category.user_id:
                abort(403, {"status" : "Access denied","state" : "Entity not accessible to current user. Provide valid name or id."})
        return func(*args, **kwargs)
    return wrapper

def ensure_auth_header(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return make_response(jsonify({
                'status': 'Failed',
                'message': 'Access is denied. Please provide request with the Authentication header.'
            }), 403)
        return func(*args, **kwargs)
    return wrapper

def token_required(f):
    """
    Decorator function to ensure that a resource is access by only authenticated users`
    provided their auth tokens are valid
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return make_response(jsonify({
                    'status': 'Failed',
                    'message': 'Provide a valid auth token'
                }), 403)

        if not token:
            return make_response(jsonify({
                'status': 'Failed',
                'message': 'Token is missing'
            }), 401)

        try:
            decode_response = User.decode_auth_token(token)
            current_user = User.query.filter_by(
                id=decode_response).first()
            if current_user:
                g.user = current_user
            else:
                return make_response(jsonify({
                    'status': 'Failed',
                    'message': "Integrity credentials for provided token are lacking."
                }), 401)
        except:
            message = 'Invalid token'
            if isinstance(decode_response, str):
                message = decode_response
            return make_response(jsonify({
                'status': 'Failed',
                'message': message
            }), 401)
        return f(current_user, *args, **kwargs)

    return decorated_function
