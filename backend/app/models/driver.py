from datetime import datetime

from app.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash


# Stores a driver's account, license, activity, and vehicle assignment.
class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True, index=True)
    phone = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey('vehicles.id'),
        unique=True,
        nullable=True,
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    vehicle = db.relationship('Vehicle', back_populates='driver')

    # Stores a password as a one-way hash.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks a password against this driver's stored hash.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Returns a concise description without exposing the password hash.
    def __repr__(self):
        return f'<Driver {self.id}: {self.license_number}>'

    # Returns this driver with JSON-safe values and no password hash.
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'license_number': self.license_number,
            'status': self.status,
            'is_active': self.is_active,
            'vehicle_id': self.vehicle_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
