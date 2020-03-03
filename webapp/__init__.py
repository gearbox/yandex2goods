from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

# Globally accessible libraries (Instances of Plugin Objects)
db = SQLAlchemy()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates',
                instance_relative_config=False)
    app.config.from_object(config.DevConfig())

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include our Routes and register blueprints
        from .main import main_routes
        from .auth import auth_routes
        from .profile import profile_routes
        app.register_blueprint(auth_routes.auth_bp)
        app.register_blueprint(main_routes.main_bp)
        app.register_blueprint(profile_routes.profile_bp)

        return app
