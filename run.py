
from app import create_app
from app.extensions import db

from app.models import Driver, Notification, Payment, Rating, User, Vehicle

app = create_app()

with app.app_context():
    print("creating tables.......")
    db.create_all()
    print("success creating tables")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)


