"""Flask config class."""
import os


class Config:
    """Set Flask default configuration vars."""

    # General Config
    FLASK_ENV = 'production'
    # FLASK_DEBUG = True
    # TESTING = os.environ.get('TESTING')
    # DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = 'my super duper mega secret key'
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024
    SERVED_FOLDER = 'static/out'
    DATABASE_URI = 'sqlite:///:memory:'


class DevConfig(Config):
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    # DEBUG = True
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError('No SECRET_KEY set for Flask application')
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
    if not DATABASE_URI:
        raise ValueError('No DATABASE_URI set for Flask application')
    # DATABASE_URI = 'sqlite:///:memory:'
    # SQLALCHEMY_DATABASE_URI =
    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_ENGINE_OPTIONS =


class ProdConfig(Config):
    FLASK_ENV = 'production'
    FLASK_DEBUG = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    # DATABASE_URI = os.environ.get('PROD_DATABASE_URI')
    # if not DATABASE_URI:
    #     raise ValueError('No DATABASE_URI set for Flask application')
    SQLALCHEMY_ECHO = False
    # SQLALCHEMY_ENGINE_OPTIONS =
