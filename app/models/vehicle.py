from datetime import datetime

from app.extensions import db


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    __table_args__ = (
        db.CheckConstraint("capacity > 0", name="ck_vehicles_capacity_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    plate_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="available")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    driver = db.relationship("Driver", back_populates="vehicle", uselist=False)

    def __repr__(self):
        return f"<Vehicle {self.plate_number} ({self.status})>"
