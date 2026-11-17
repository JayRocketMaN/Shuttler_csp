
from datetime import datetime, timedelta
from app.extensions import db
from app.models.trip import Trip
from app.models.route import Route


def create_new_trip(data):   
    route_id = data.get('route_id')
    driver_id = data.get('driver_id')
    vehicle_id = data.get('vehicle_id')
    departure_time_str = data.get('departure_time')

    if not route_id or not driver_id or not vehicle_id or not departure_time_str:
        return None, 'missing required data'

    route = Route.query.get(route_id)

    if not route:
        return None, 'No route found'

    try:
        departure_time = datetime.fromisoformat(departure_time_str)

    except ValueError:
        return None, 'invalid date format'

    # checking if there is a trip for this vehicle or driver within 1 hour of the new time
    time_window_start = departure_time - timedelta(hours = 1)
    time_window_end = departure_time + timedelta(hours = 1)

    vehicle_conflict = Trip.query.filter(
        Trip.vehicle_id == vehicle_id,
        Trip.departure_time >= time_window_start,
        Trip.departure_time <= time_window_end
    ).first()

    if vehicle_conflict:
        return None, 'this vehicle is already schedul for another trip around this time'

    driver_conflict = Trip.query.filter(
        Trip.driver_id == driver_id,
        Trip.departure_time >= time_window_start,
        Trip.departure_time <= time_window_end
    ).first()

    if driver_conflict:
        return None, "this driver is already schedul for another trip around this time"


    new_trip = Trip(
         route_id = route_id,
        driver_id = driver_id,
        vehicle_id = vehicle_id,
        departure_time = departure_time,
        status = "SCHEDULED"
    )

    try:

        db.session.add(new_trip)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('DB Error: ', e)
        
        return None, 'database error while creating trip'

    return new_trip, None



