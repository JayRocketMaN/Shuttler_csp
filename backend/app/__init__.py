import os

from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from app.extensions import db, migrate

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ourSecretKey')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', app.config['SECRET_KEY'])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    from app.routes.booking import booking_bp
    from app.routes.payment import payment_bp

    app.register_blueprint(booking_bp)
    app.register_blueprint(payment_bp)

    # Import models here so Alembic registers them during schema generation
    with app.app_context():
        from app import models

    return app
