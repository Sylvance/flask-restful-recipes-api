#!/usr/bin/env python

import functools
from flask import request, url_for, abort, json
from code.models.recipe import Recipe
from code.models.category import Category


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

def abort_if_exists(user_id, category_name=None, category_id=None, recipe_name=None):
    category = None
    recipe = None
    if category_name:
        categories = Category.get_user_all(user_id)
        categorylist = []
        for category in categories:
            categorylist.append(category.title)
        if category_name in categorylist:
            abort(400, {"status" : "Bad request","state" : "Category already exists"})
    if recipe_name:
        category = Category.get_by_id(category_id)
        if category.user_id == user_id:
            if Recipe.recipe_exists(category_id, recipe_name):
                abort(400, {"status" : "Bad request","state" : "Recipe already exists"})
        else:
            abort(403, {"status" : "Access denied","state" : "Category does not belong to this user"})
