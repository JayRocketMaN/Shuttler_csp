from datetime import datetime
from app.models import db

class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    vehicle_number = db.Column(db.String(50), nullable=False)
    driver_name = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), default='SCHEDULED')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    route = db.relationship('Route', back_populates='trips')

    def __repr__(self):
        return f"<Trip id={self.id}, vehicle='{self.vehicle_number}', status='{self.status}'>"

    def to_dict(self):
        return {
            "id": self.id,
            "route_id": self.route_id,
            "vehicle_number": self.vehicle_number,
            "driver_name": self.driver_name,
            "departure_time": self.departure_time.isoformat() if self.departure_time else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }