from datetime import datetime

from app.extensions import db


# Stores a scheduled trip, its route, driver, and booking capacity.
class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    vehicle_number = db.Column(db.String(50), nullable=False)
    driver_name = db.Column(db.String(100), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    departure_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), default='SCHEDULED')
    capacity = db.Column(db.Integer)
    booked_count = db.Column(db.Integer, default=0)
    price = db.Column(db.Numeric(10, 2))
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    route = db.relationship('Route', back_populates='trips')

    # Returns a concise description of this trip.
    def __repr__(self):
        return (
            f'<Trip id={self.id}, vehicle=\'{self.vehicle_number}\', '
            f'status=\'{self.status}\'>'
        )

    # Returns this trip with JSON-safe values.
    def to_dict(self):
        return {
            'id': self.id,
            'route_id': self.route_id,
            'vehicle_number': self.vehicle_number,
            'driver_name': self.driver_name,
            'driver_id': self.driver_id,
            'departure_time': self.departure_time.isoformat() if self.departure_time else None,
            'status': self.status,
            'capacity': self.capacity,
            'booked_count': self.booked_count,
            'price': str(self.price) if self.price is not None else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
