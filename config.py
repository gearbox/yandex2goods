"""Flask config class."""
from os import environ
from pathlib import Path


project_dir = Path(__file__).parent


class Config:
    """Set Flask default configuration vars."""
    SESSION_COOKIE_NAME = 'lgn'
    SECRET_KEY = environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError('No SECRET_KEY set for Flask application')
    # STATIC_URL_PATH = ''
    # STATIC_FOLDER = 'static'
    # TEMPLATES_FOLDER = 'templates'
    SERVED_FOLDER = project_dir / 'converted'
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    DEBUG = True
    TESTING = True
    # SQLA: [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_SQLA_DATABASE_URI')
    if not SQLALCHEMY_DATABASE_URI:
        # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_ENGINE_OPTIONS =


class ProdConfig(Config):
    FLASK_ENV = 'production'
    FLASK_DEBUG = False
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_SQLA_DATABASE_URI')
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_ECHO = False
