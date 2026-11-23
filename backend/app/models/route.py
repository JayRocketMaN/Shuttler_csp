from datetime import datetime

from app.extensions import db
from app.models.route_stop import RouteStop


# Stores a named route and its ordered bus stops.
class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    route_stops = db.relationship(
        'RouteStop',
        back_populates='route',
        cascade='all, delete-orphan',
        order_by='RouteStop.stop_order',
    )
    trips = db.relationship(
        'Trip',
        back_populates='route',
        cascade='all, delete-orphan',
    )

    # Returns a concise description of this route.
    def __repr__(self):
        return f'<Route id={self.id}, name=\'{self.name}\', active={self.is_active}>'

    # Returns this route and its bus stops with JSON-safe values.
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'stops': [route_stop.to_dict() for route_stop in self.route_stops],
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
