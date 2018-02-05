#!/usr/bin/env python

import datetime
import jwt
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from code.database import (
    db,
    Model,
    SurrogatePK,
    relationship,
)
from .category import Category
from .token import Token


class User(SurrogatePK, Model):
    __tablename__ = 'users'
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime(256), nullable=False)
    modified_at = db.Column(db.DateTime(256), nullable=False)

    categories = relationship(Category, cascade="all, delete-orphan", backref=db.backref('user'))

    def __init__(self, username, email, password, **kwargs):
        db.Model.__init__(self, username=username, email=email,
                          password=password, **kwargs)
        self.set_password(password)
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password_hash, value)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30,seconds=3600),
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
            is_banned_token = Token.check_banned(auth_token)
            if is_banned_token:
                return 'Banned Token. Please sign in again.'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired Signature. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):  # pragma: nocover
        return '<User({username!r})>'.format(username=self.username)
