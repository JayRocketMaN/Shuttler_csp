# Import all models so Flask-Migrate / Alembic discovers them
from app.models.location import Location
from app.models.bus_stop import BusStop
from app.models.route import Route, RouteStop
from app.models.trip import Trip
from backend.app.models.payment import Payment
from backend.app.models.rating import Rating
from backend.app.models.notification import Notification
from backend.app.models import Driver,User, Vehicle
