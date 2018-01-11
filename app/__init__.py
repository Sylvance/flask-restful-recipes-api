""" This main application initialisation """
import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api, fields
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from common.config import app_config

# Initialize the database
db = SQLAlchemy()
# Ensure password encryption
bcrypto = Bcrypt() 

# Marshaled fields for links in meta section
link_fields = {
    'prev': fields.String,
    'next': fields.String,
    'first': fields.String,
    'last': fields.String,
}

# Marshaled fields for meta section
meta_fields = {
    'page': fields.Integer,
    'limit': fields.Integer,
    'total': fields.Integer,
    'pages': fields.Integer,
    'links': fields.Nested(link_fields)
}

def create_app():
    # Initialize application
	app = Flask(__name__)
	config_name = os.getenv('FLASK_CONFIG')
	app.config.from_object(app_config[config_name])

	# Initialize the API
	api = Api(app)
	db.init_app(app)
	bcrypto.init_app(app)

	# Initialize Flask Migrate
	migrate = Migrate(app, db)
	# Models
	from app.models import UserModel, CategoryModel, RecipeModel

	# Resources
	from app.resources.user import User, UserList, SignupUser, SigninUser, SignoutUser, ResetPassword
	from app.resources.category import Category, CategoryList
	from app.resources.recipe import Recipe, RecipeList

	@app.route('/')
	@app.route('/index')
	def index():
	    """ Here the user sees the signup and signin gateways """
	    return render_template('index.html',
	                           title='Home')

	api.add_resource(CategoryList, '/api/v1/categories')
	api.add_resource(RecipeList, '/api/v1/recipes')
	api.add_resource(UserList, '/api/v1/users')
	api.add_resource(SignupUser, '/api/v1/signup')
	api.add_resource(SigninUser, '/api/v1/signin')
	api.add_resource(SignoutUser, '/api/v1/signout')
	api.add_resource(Category, '/api/v1/category/<int:categoryid>')
	api.add_resource(Recipe, '/api/v1/recipe/<int:recipeid>')
	api.add_resource(User, '/api/v1/user/<int:userid>')
	api.add_resource(ResetPassword, '/api/v1/resetpassword/user/<int:userid>')

	# Enabling cors
	CORS(app)	

	return app
