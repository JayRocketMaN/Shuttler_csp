from datetime import datetime
from app.extensions import db


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable = False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable = False)


    departure_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), default='SCHEDULED')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    route = db.relationship('Route', back_populates = 'trips')
    driver = db.relationship('Driver')
    vehicle = db.relationship('Vehicle')

    def __repr__(self):
        return f"<Trip id={self.id}, vehicle='{self.vehicle_number}', status='{self.status}'>"

    def to_dict(self):
        return {
            "id": self.id,
            "route_id": self.route_id,

            "driver_id": self.driver_id,
            # "driver_name": self.driver_name.full_name if self.driver else None,

            "vehicle_id": self.vehicle_id,
            "vehicle_plate": self.vehicle.plate_number if self.vehicle else None,  # returns null if driver is deleted

            "departure_time": self.departure_time.isoformat() if self.departure_time else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }