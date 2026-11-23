feat/models
import os

from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from app.extensions import db, migrate
from flask import Flask
from datetime import timedelta
from config import Config
from app.extensions import db, migrate, jwt
dev

from app.routes.auth_routes import auth_bp
from app.routes.booking_routes import booking_bp
from app.routes.trip_routes import trip_bp
from app.routes.vehicle_routes import vehicle_bp
from app.routes.driver_routes import driver_bp
from app.routes.bus_stop_routes import bus_stop_bp
from app.routes.route_routes import route_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours = 24)

feat/models
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

    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError('No DATABASE_URL in .env file')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Blueprint Registration
    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(trip_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(driver_bp)
    app.register_blueprint(bus_stop_bp)
    app.register_blueprint(route_bp)

    from app.routes.notifications import notifications

    app.register_blueprint(notifications, url_prefix='/notifications')

    from app.routes.notifications import notifications

    app.register_blueprint(notifications, url_prefix='/notifications')
dev

    # Import models here so Alembic registers them during schema generation
    # with app.app_context():
    #     from app import models

    return app
