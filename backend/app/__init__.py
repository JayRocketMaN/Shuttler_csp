from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt
from app.routes.auth_routes import auth_bp
from app.routes.booking_routes import booking_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError('No DATABASE_URL in .env file')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Blueprint Registration
    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)

    from app.routes.notifications import notifications

    app.register_blueprint(notifications, url_prefix='/notifications')

    
    with app.app_context():  # importing models here so Alembic registers them in db
        from app import models

    return app