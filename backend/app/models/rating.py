from datetime import datetime

from app.extensions import db


# Stores a passenger's feedback for a trip and its driver.
class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, nullable=False)
    trip_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Returns a concise description of this rating.
    def __repr__(self):
        return f'<Rating {self.score}/5 for Trip {self.trip_id}>'

    # Returns this rating with JSON-safe values.
    def to_dict(self):
        return {
            'id': self.id,
            'passenger_id': self.passenger_id,
            'driver_id': self.driver_id,
            'trip_id': self.trip_id,
            'score': self.score,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
