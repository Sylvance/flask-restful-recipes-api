#!/usr/bin/env python

import os


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG = True

    ERROR_404_HELP = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'xoi82SJuX98#*$aIAjakj3sus')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql:///recipesdemo')
    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql:///recipesdemo')


class TestConfig(Config):
    """Test configuration."""
    ENV = 'test'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///recipesdemotest'
