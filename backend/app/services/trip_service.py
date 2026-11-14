
from datetime import datetime
from app.extensions import db
from app.models.trip import Trip
from app.models.route import Route


def create_new_trip(data):   
    route_id = data.get('route_id')
    route = Route.query.get(route_id)

    if not route:
        return None, 'No Route was found. Please create the route first'

    vehicle_number = data.get('vehicle_number')
    driver_name = data.get('driver_name')
    departure_time_str = data.get('departure_time')

    if not vehicle_number or not driver_name or not departure_time_str:
        return None, 'missing required fields data (vehicle_number, driver_name, departure_time)'

    try:
        # Expecting format: "2026-11-20T08:30:00"
        departure_time = datetime.fromisoformat(departure_time_str)
    except ValueError:
        return None, 'invalid date format. use YYYY-MM-DDTHH:MM:SS'

    new_trip = Trip(
        route_id = route_id,
        vehicle_number = vehicle_number,
        driver_name = driver_name,
        departure_time = departure_time,
        status = "SCHEDULED"
    )

    try:

        db.session.add(new_trip)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('DB Error: ', e)
        
        return None, 'Database error while creating trip'

    return new_trip, None



