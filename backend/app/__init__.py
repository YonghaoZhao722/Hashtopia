# backend/app/__init__.py
from flask import Flask
from config import config
from app.extensions import db, jwt, cors
from app.routes.user import user_bp
from flask_migrate import Migrate
import os

migrate = Migrate()
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.post import post_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(post_bp, url_prefix='/api/posts')
    app.register_blueprint(user_bp, url_prefix='/api')

    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app