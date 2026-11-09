from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt
from app.routes.auth_routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError('No DATABASE_URL in .env file')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)

    from app.routes.notifications import notifications

    app.register_blueprint(notifications, url_prefix='/notifications')

    # Import models here so Alembic registers them during schema generation
    # with app.app_context():
    #     from app import models

    return app