from backend.app.extensions import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)

    booking_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, nullable = False)   # I hv used plain intergers for now coz they are foreignkeys(booking_id & user_id) which i have to link from u guys own task

    amount = db.Column(db.Numeric(10, 2), nullable = False)
    currency = db.Column(db.String(20), default = 'NGN')
    payment_method = db.Column(db.String(50), nullable = 'False') # e,g card, transfer

    transaction_reference = db.Column(db.String(100), unique = True, nullable = False)   # paystack

    status = db.Column(db.String(20), default = 'pending') # pending, success, failed

    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

    def __repr__(self):
        return f"<Payment {self.transaction_reference} - {self.status}>"

      