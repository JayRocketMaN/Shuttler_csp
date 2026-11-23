from datetime import datetime

from app.extensions import db


# Stores the latest live position and motion details for one trip.
class TripLocation(db.Model):
    __tablename__ = 'trip_locations'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(
        db.Integer,
        db.ForeignKey('trips.id'),
        unique=True,
        nullable=False,
    )
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    heading = db.Column(db.Float)
    speed = db.Column(db.Float)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Returns a concise description of this trip's latest position.
    def __repr__(self):
        return f'<TripLocation {self.id} for Trip {self.trip_id}>'

    # Returns this trip position with JSON-safe values.
    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'heading': self.heading,
            'speed': self.speed,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
