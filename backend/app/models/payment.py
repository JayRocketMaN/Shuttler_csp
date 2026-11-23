from datetime import datetime

from app.extensions import db


# Stores payment details for a booking.
class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(
        db.Integer,
        db.ForeignKey('bookings.id'),
        nullable=False,
    )
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(20), default='NGN')
    payment_method = db.Column(db.String(50), nullable=True)
    reference = db.Column(db.String(100), unique=True)
    transaction_reference = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
    )
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Returns a concise description of this payment.
    def __repr__(self):
        return f'<Payment {self.transaction_reference} - {self.status}>'

    # Returns this payment with JSON-safe values.
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'user_id': self.user_id,
            'amount': str(self.amount) if self.amount is not None else None,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'reference': self.reference,
            'transaction_reference': self.transaction_reference,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
