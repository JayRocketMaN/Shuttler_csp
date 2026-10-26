from datetime import datetime
from app.models import db

class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    route_stops = db.relationship('RouteStop', back_populates='route', cascade='all, delete-orphan', order_by='RouteStop.stop_order')
    trips = db.relationship('Trip', back_populates='route', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Route id={self.id}, name='{self.name}', active={self.is_active}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "stops": [rs.to_dict() for rs in self.route_stops],
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class RouteStop(db.Model):
    __tablename__ = 'route_stops'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    bus_stop_id = db.Column(db.Integer, db.ForeignKey('bus_stops.id'), nullable=False)
    stop_order = db.Column(db.Integer, nullable=False)

    # Relationships
    route = db.relationship('Route', back_populates='route_stops')
    bus_stop = db.relationship('BusStop', backref='route_associations')

    def __repr__(self):
        return f"<RouteStop id={self.id}, route_id={self.route_id}, bus_stop_id={self.bus_stop_id}, order={self.stop_order}>"

    def to_dict(self):
        return {
            "id": self.id,
            "stop_order": self.stop_order,
            "bus_stop": self.bus_stop.to_dict() if self.bus_stop else None
        }