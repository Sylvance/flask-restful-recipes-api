""" Model for the User class """
import os
import jwt
import datetime
from app import db, bcrypto
from flask import current_app as app
from flask_restful import url_for


class UserModel(db.Model):
    """ User class"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)
    categories = db.relationship(
        'CategoryModel', backref='UserModel', lazy=True)

    def __init__(self, username, email, bio, password):
        """ Construct the user """
        config_name = os.getenv('FLASK_CONFIG')
        self.username = username
        self.email = email
        self.bio = bio
        self.password = bcrypto.generate_password_hash(
            password, app.config['BCRYPT_LOG_ROUNDS']
        ).decode()
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=app.config['AUTH_TOKEN_EXPIRY_DAYS'],
                                                                       seconds=app.config[
                                                                           'AUTH_TOKEN_EXPIRY_SECONDS']),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token,
                                 app.config['SECRET_KEY'],
                                 algorithms='HS256')
            is_banned_token = BannedToken.check_banned(auth_token)
            if is_banned_token:
                return 'Banned Token. Please sign in again.'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired Signature. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def save(self):
        """ Persist the user in the database :param user: :return: """
        db.session.add(self)
        db.session.commit()
        return self.encode_auth_token(self.id)

    @staticmethod
    def get_all():
        """ Get all users """
        USERS = UserModel.query
        return USERS

    @staticmethod
    def get_by_id(user_id):
        """ Filter a user by Id. :param user_id: :return: User or None """
        user = UserModel.query.filter_by(id=user_id).first()
        return user

    @staticmethod
    def get_by_email(email):
        """ Check a user by their email address :param email: :return: """
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return None
        return user

    def reset_password(self, new_password):
        """ Update/reset the user password. :param new_password: New User Password :return: """
        self.password = bcrypto.generate_password_hash(new_password, app.config['BCRYPT_LOG_ROUNDS']) \
            .decode('utf-8')
        self.modified_at = datetime.datetime.now()
        db.session.commit()
        return self

    def update(self, username, email, bio):
        """ Update the user :param username: :param email: :param bio: :return: """
        self.username = username
        self.email = email
        self.bio = bio
        self.modified_at = datetime.datetime.now()
        db.session.commit()
        return self

    def delete(self):
        """ Delete a user from the database :return: """
        db.session.delete(self)
        db.session.commit()


class BannedToken(db.Model):
    """
    Token Model for storing JWT tokens
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    banned_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.banned_on = datetime.datetime.now()

    def banned(self):
        """
        Persist Banned token in the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_banned(auth_token):
        # check whether auth token has been banned
        res = BannedToken.query.filter_by(token=auth_token).first()
        if res:
            return True
        return False

""" Model for category class """


class CategoryModel(db.Model):
    """Category Model class"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categorytitle = db.Column(db.String(255), nullable=False)
    categorydescription = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)
    recipes = db.relationship(
        'RecipeModel', backref='CategoryModel', lazy=True)

    def __init__(self, categorytitle, categorydescription, user_id):
        """Category object constructor"""
        self.categorytitle = categorytitle
        self.categorydescription = categorydescription
        self.user_id = user_id
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        """ Persist the category in the database :param category: :return: """
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_all():
        """ Get all categories """
        CATEGORIES = CategoryModel.query
        return CATEGORIES

    @staticmethod
    def get_by_id(category_id):
        """ Filter a category by Id. :param category_id: :return: Category or None """
        category = CategoryModel.query.filter_by(id=category_id).first()
        return category

    @staticmethod
    def get_by_title(categorytitle):
        """ Check a category by their categorytitle :param categorytitle: :return: """
        category = CategoryModel.query.filter_by(
            categorytitle=categorytitle).first()
        return category

    def update(self, categorytitle, categorydescription):
        """ Update the category :param categorytitle: categorydescription:return: """
        self.categorytitle = categorytitle
        self.categorydescription = categorydescription
        self.modified_at = datetime.datetime.now()
        db.session.commit()
        return self

    def delete(self):
        """ Delete a category from the database :return: """
        db.session.delete(self)
        db.session.commit()

""" Model for recipes class """


class RecipeModel(db.Model):
    """ Recipe Model class """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipetitle = db.Column(db.String(255), nullable=False)
    recipedescription = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey(CategoryModel.id))
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, recipetitle, recipedescription, category_id):
        """ Construct recipe"""
        self.recipetitle = recipetitle
        self.recipedescription = recipedescription
        self.category_id = category_id
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        """ Persist the recipe in the database :param recipe: :return: """
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_all():
        """ Get all recipes """
        RECIPES = RecipeModel.query
        return RECIPES

    @staticmethod
    def get_by_id(recipe_id):
        """ Filter a recipe by Id. :param recipe_id: :return: Recipe or None """
        recipe = RecipeModel.query.filter_by(id=recipe_id).first()
        return recipe

    def update(self, recipetitle, recipedescription):
        """ Update the recipe :param recipetitle: recipedescription:return: """
        self.recipetitle = recipetitle
        self.recipedescription = recipedescription
        self.modified_at = datetime.datetime.now()
        db.session.commit()
        return self

    def delete(self):
        """ Delete a recipe from the database :return: """
        db.session.delete(self)
        db.session.commit()
