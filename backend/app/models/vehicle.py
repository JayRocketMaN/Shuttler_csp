from datetime import datetime

from app.extensions import db


# Stores a vehicle's identifying details, capacity, and availability.
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    __table_args__ = (
        db.CheckConstraint('capacity > 0', name='ck_vehicles_capacity_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    plate_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    driver = db.relationship('Driver', back_populates='vehicle', uselist=False)

    # Returns a concise description of this vehicle.
    def __repr__(self):
        return f'<Vehicle {self.plate_number} ({self.status})>'

    # Returns this vehicle with JSON-safe values.
    def to_dict(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'plate_number': self.plate_number,
            'capacity': self.capacity,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
