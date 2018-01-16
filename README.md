[![Build Status](https://travis-ci.org/Sylvance/flask-restful-recipes-api.svg?branch=master)](https://travis-ci.org/Sylvance/flask-restful-recipes-api)
[![Coverage Status](https://coveralls.io/repos/github/Sylvance/flask-restful-recipes-api/badge.svg?branch=develop)](https://coveralls.io/github/Sylvance/flask-restful-recipes-api?branch=develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f24714bd15134063aec24f1e74c9be79)](https://www.codacy.com/app/Sylvance/flask-restful-recipes-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Sylvance/flask-restful-recipes-api&amp;utm_campaign=Badge_Grade)

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
        

Resources
---------

| Col A | Col B | Col C|
|---|---|---|
| A1 | B1 | C1 |
| A2 |  | :smile: |


