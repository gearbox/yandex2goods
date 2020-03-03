"""Flask config class."""
from os import environ


class Config:
    """Set Flask default configuration vars."""
    SESSION_COOKIE_NAME = 'lgn'
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    # STATIC_URL_PATH = '',
    # STATIC_FOLDER = 'static'
    # TEMPLATES_FOLDER = 'templates'
    SERVED_FOLDER = 'converted'
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024
    DATABASE_URI = 'sqlite:///:memory:'


class DevConfig(Config):
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    DEBUG = True
    TESTING = True
    SECRET_KEY = environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError('No SECRET_KEY set for Flask application')
    DATABASE_URI = environ.get('DEV_DATABASE_URI')
    if not DATABASE_URI:
        raise ValueError('No DATABASE_URI set for Flask application')
    # SQLALCHEMY_DATABASE_URI =
    # SQLALCHEMY_ECHO = True
    # SQLALCHEMY_ENGINE_OPTIONS =


class ProdConfig(Config):
    FLASK_ENV = 'production'
    FLASK_DEBUG = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    DATABASE_URI = environ.get('PROD_DATABASE_URI')
    if not DATABASE_URI:
        raise ValueError('No DATABASE_URI set for Flask application')
    # SQLALCHEMY_ECHO = False
    # SQLALCHEMY_ENGINE_OPTIONS =
