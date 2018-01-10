"""
Helper file
"""

import functools
from functools import wraps
from flask import request, url_for, make_response, jsonify
from flask_restful import abort
from app.models import UserModel, CategoryModel, RecipeModel


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
                })), 403

        if not token:
            return make_response(jsonify({
                'status': 'Failed',
                'message': 'Token is missing'
            })), 401

        try:
            decode_response = UserModel.decode_auth_token(token)
            current_user = UserModel.query.filter_by(
                id=decode_response).first()
        except:
            message = 'Invalid token'
            if isinstance(decode_response, str):
                message = decode_response
            return make_response(jsonify({
                'status': 'Failed',
                'message': message
            })), 401

        return f(current_user, *args, **kwargs)

    return decorated_function


def user_only(f):
    """
    Decorator function to ensure that a resource is accessed by 
    the user than is logged in
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user:
            if kwargs.get('username', None):
                if current_user['username'] != kwargs['username']:
                    abort(403)
            if kwargs.get('user_id', None):
                if current_user['id'] != kwargs['user_id']:
                    abort(403)
        return f(*args, **kwargs)

    return decorated_functions


def abort_if_user_doesnt_exist(userid):
    """ Make an abort helper 
        :param userid: Userid 
        :abort with message: 
    """
    result = UserModel.get_by_id(userid)
    if result is None:
        abort(404, message="User {} doesn't exist".format(userid))


def abort_if_category_doesnt_exist(categoryid):
    """ Make an abort helper 
        :param categoryid: categoryid 
        :abort with message: 
    """
    result = CategoryModel.get_by_id(categoryid)
    if result is None:
        abort(404, message="Category {} doesn't exist".format(categoryid))


def abort_if_recipe_doesnt_exist(recipeid):
    """ Make an abort helper 
        :param recipeid: recipeid 
        :abort with message: 
    """
    result = RecipeModel.get_by_id(recipeid)
    if result is None:
        abort(404, message="Recipe {} doesn't exist".format(recipeid))


def respond(status, status_code, message, auth_token=None):
    """ Make an respond helper 
        :param item: item 
        :abort with message: 
    """
    if auth_token == None:
        json = jsonify({
            'status': '{}'.format(status),
            'status code': '{}'.format(status_code),
            'message': '{}'.format(message)
        })
        json.status_code = status_code
    else:
        json = jsonify({
            'status': '{}'.format(status),
            'status code': '{}'.format(status_code),
            'message': '{}'.format(message),
            'auth_token': '{}'.format(auth_token)
        })
        json.status_code = status_code
    return json


def paginate(max_limit=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            page = request.args.get('page', 1, type=int)
            limit = min(request.args.get('limit', max_limit,
                                            type=int),
                           max_limit)

            query = func(*args, **kwargs)
            p = query.paginate(page, limit)

            meta = {
                'page': page,
                'limit': limit,
                'total': p.total,
                'pages': p.pages,
            }

            links = {}
            if p.has_next:
                links['next'] = url_for(request.endpoint, page=p.next_num,
                                        limit=limit, **kwargs)
            if p.has_prev:
                links['prev'] = url_for(request.endpoint, page=p.prev_num,
                                        limit=limit, **kwargs)
            links['first'] = url_for(request.endpoint, page=1,
                                     limit=limit, **kwargs)
            links['last'] = url_for(request.endpoint, page=p.pages,
                                    limit=limit, **kwargs)

            meta['links'] = links
            result = {
                'items': p.items,
                'meta': meta
            }

            return result, 200
        return wrapped
    return decorator
