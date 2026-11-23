from app.extensions import db


# Connects a bus stop to a route at a specific position.
class RouteStop(db.Model):
    __tablename__ = 'route_stops'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    bus_stop_id = db.Column(db.Integer, db.ForeignKey('bus_stops.id'), nullable=False)
    stop_order = db.Column(db.Integer, nullable=False)

    route = db.relationship('Route', back_populates='route_stops')
    bus_stop = db.relationship('BusStop', backref='route_associations')

    # Returns a concise description of this route stop.
    def __repr__(self):
        return (
            f'<RouteStop id={self.id}, route_id={self.route_id}, '
            f'bus_stop_id={self.bus_stop_id}, order={self.stop_order}>'
        )

    # Returns this route stop with its bus stop as JSON-safe values.
    def to_dict(self):
        return {
            'id': self.id,
            'stop_order': self.stop_order,
            'bus_stop': self.bus_stop.to_dict() if self.bus_stop else None,
        }
