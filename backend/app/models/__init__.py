# Import all models so Flask-Migrate / Alembic discovers them
from app.models.location import Location
from app.models.bus_stop import BusStop
from app.models.route import Route, RouteStop
from app.models.trip import Trip
from app.models.payment import Payment
from app.models.rating import Rating
from app.models.notification import Notification
from app.models.driver import Driver
from app.models.user import User
from app.models.vehicle import Vehicle