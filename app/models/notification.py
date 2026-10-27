
from app.extensions import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, nullable = False)  # the person receiving the notification

    title = db.Column(db.String(100), nullable = False)
    message = db.Column(db.Text, nullable = False)

    type = db.Column(db.String(50), default = 'system') # the type of notification can be: booking, payment, trip_update or system

    is_read = db.Column(db.Boolean, default = False)

    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"<Notification {self.title} for User {self.user_id}>"
      




