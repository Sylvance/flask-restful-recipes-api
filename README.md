[![Build Status](https://travis-ci.org/Sylvance/flask-restful-recipes-api.svg?branch=master)](https://travis-ci.org/Sylvance/flask-restful-recipes-api)
[![Coverage Status](https://coveralls.io/repos/github/Sylvance/flask-restful-recipes-api/badge.svg?branch=develop)](https://coveralls.io/github/Sylvance/flask-restful-recipes-api?branch=develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f24714bd15134063aec24f1e74c9be79)](https://www.codacy.com/app/Sylvance/flask-restful-recipes-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Sylvance/flask-restful-recipes-api&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/47bc65ffe1ce52ed9797/maintainability)](https://codeclimate.com/github/Sylvance/flask-restful-recipes-api/maintainability)

# Flask-restful-recipes-api
Yummy recipes provides a platform for users to keep track of their awesome recipes and share with others if they so wish.

## Installation

Virtualenv required. Using virtualenv-wrapper for windows

### create virtual environment
```
# create virtual environment
mkvirtualenv recipes-api
cd recipes-api
```

### clone the repo
```
# clone the repo
git clone https://github.com/Sylvance/flask-restful-recipes-api.git
cd flask-restful-recipes-api
```

### install requirements
```
# install requirements
pip install -r requirements.txt
```

### test
```
# test
cd tests
set FLASK_CONFIG=testing #for windows
		or
export FLASK_CONFIG=testing #for others
python test.py
```

### run
```
# run
set FLASK_CONFIG=development #for windows
		or
export FLASK_CONFIG=development #for others
set FLASK_APP=run.py #for windows
		or
export FLASK_APP=run.py #for others
flask run
```

## Tree stucture
To build a tree structure diagram in windows run this command;
```tree /F /A > tree.txt```

```
|   .coverage
|   .coveralls.yml
|   .gitignore
|   .travis.yml
|   LICENSE
|   README.md
|   requirements.txt
|   run.py
|   test.py
|   tree.txt
|   
+---app
|   |   models.py
|   |   __init__.py
|   |   
|   +---resources
|   |   |   category.py
|   |   |   helper.py
|   |   |   recipe.py
|   |   |   user.py
|   |   |   __init__.py
|   |   
|
+---common
|   |   config.py
|   |   __init__.py
|           
+---cover
|       
+---migrations     
```

Resources
---------

## Documentation for API Endpoints

All URIs are relative to *https://resapi.herokuapp.com/api*

|---| Endpoint | Description|
|---|---|---|
|---| **GET** /users/`{id}`/categories | List all available categories
|---| **POST** /users/`{id}`/categories | Create a new category to the list.
|---| **GET** /categories/`{id}`/recipes | List all available recipes
|---| **POST** /categories/`{id}`/recipes | Create a new recipe to the list.
|---| **DELETE** /users/`{user_id}`/categories/`{category_id}` | Remove a single category by id
|---| **GET** /users/`{user_id}`/categories/`{category_id}` | Get a single category by id
|---| **POST** /users/`{user_id}`/categories/`{category_id}` | Update a single category by id
|---| **DELETE** /categories/`{category_id}`/recipes/`{recipe_id}` | Remove a single recipe by id
|---| **GET** /categories/`{category_id}`/recipes/`{recipe_id}` | Get a single recipe by id
|---| **POST** /categories/`{category_id}`/recipes/`{recipe_id}` | Update a single recipe by id
|---| **POST** /users | Sign up a user
|---| **POST** /users/signin | Sign in a user
|---| **GET** /users/signout | Sign out a user
| :joy: | :open_mouth: | :smile: |
