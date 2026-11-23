from datetime import datetime

from app.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash


# Stores a passenger or administrator account and its contact details.
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    # email = db.Column(db.String(255), unique=True, nullable=True, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)  # change email nullable to False since we register with email and also filter by email
    phone = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Stores a password as a one-way hash.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks a password against this user's stored hash.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Returns a concise description without exposing the password hash.
    def __repr__(self):
        return f'<User {self.id}: {self.phone}>'

    # Returns this user with JSON-safe values and no password hash.
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
