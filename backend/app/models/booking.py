from datetime import datetime
from app.extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)

    pickup_location = db.Column(db.String(255), nullable = False)
    dropoff_location = db.Column(db.String(255), nullable = False)
    seat_count = db.Column(db.Integer, default = 1)
    total_amount = db.Column(db.Numeric(10, 2), nullable = False)


    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref="bookings")
    trip = db.relationship("Trip", backref="bookings")

    