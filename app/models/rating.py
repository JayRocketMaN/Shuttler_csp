
from app.extensions import db
from datetime import datetime

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key = True)

    passenger_id = db.Column(db.Integer, nullable = False)
    driver_id = db.Column(db.Integer, nullable = False)   # passenger and driver to know who did the rating

    trip_id = db.Column(db.Integer, nullable = False)    # link to specific trip rated 

    score = db.Column(db.Integer, nullable = False)  # out of 5

    comment = db.Column(db.Text, nullable = True)  # optional

    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"<Rating {self.score}/5 for Trip {self.trip_id}>"






