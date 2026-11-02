import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate, jwt
from app.routes.auth_routes import auth_bp

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
load_dotenv(os.path.join(base_dir, '.env'))

def create_app():
    app = Flask(__name__)

    database_url = os.getenv('DATABASE_URL')
    print(f"----- CONNECTING TO DB: {database_url} ----")

    if not database_url:
        raise ValueError('No DATABASE_URL in .env file')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ourSecretKey')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)

    # Import models here so Alembic registers them during schema generation
    # with app.app_context():
    #     from app import models

    return app