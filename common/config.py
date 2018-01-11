""" 
    The configuration file for;
        1. Development
        2. Testing
        3. Production 
"""
import os

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'xoi82SJuX98#*$aIAjakj3sus')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql:///recipes')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    BCRYPT_LOG_ROUNDS = 14
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 3000
    PAGINATION = 4


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    AUTH_TOKEN_EXPIRY_DAYS = 1
    AUTH_TOKEN_EXPIRY_SECONDS = 20
    SQLALCHEMY_DATABASE_URI = 'postgresql:///recipes'


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 20

class TestingConfig(Config):
    """
    Testing configurations
    """

    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    AUTH_TOKEN_EXPIRY_DAYS = 0
    AUTH_TOKEN_EXPIRY_SECONDS = 3
    AUTH_TOKEN_EXPIRATION_TIME_DURING_TESTS = 5
    SQLALCHEMY_DATABASE_URI = 'postgresql:///recipestest'

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
