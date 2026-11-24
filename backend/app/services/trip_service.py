
from datetime import datetime, timedelta
from sqlalchemy import or_
from datetime import datetime

from app.extensions import db

from app.models.trip import Trip
from app.models.route import Route, RouteStop
from app.models.bus_stop import BusStop


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


def search_trips(pickup_name, dropoff_name):

    # finding the ids of bust stops that match name
    pickup_stops = BusStop.query.filter(
        BusStop.name.ilike(f"%{pickup_name}%")
    ).all()

    dropoff_stops = BusStop.query.filter(
        BusStop.name.ilike(f"%{dropoff_name}%")
    ).all()

    if not pickup_stops or not dropoff_stops:
        return []                   # no stops found for those names

    pickup_ids = []
    for stop in pickup_stops:
        pickup_ids.append(stop.id)

    dropoff_ids = []
    for stop in dropoff_stops:
        dropoff_ids.append(stop.id)

    routes_with_pickup = RouteStop.query.filter(   # routes that hv both pickup stop & dropoff stop, or routes that pass through those stops
        RouteStop.bus_stop_id.in_(pickup_ids)
    ).all()

    routes_with_dropoff = RouteStop.query.filter(
        RouteStop.bus_stop_id.in_(dropoff_ids)
    ).all()

    pickup_route_ids = []         # collectx routes ids 
    for rs in routes_with_pickup:
        pickup_route_ids.append(rs.route_id)

    dropoff_route_ids = []
    for rs in routes_with_dropoff:
        dropoff_route_ids.append(rs.route_id)

    matching_route_ids = []
    for route_id in pickup_route_ids:
        if route_id in dropoff_route_ids:

            if route_id not in matching_route_ids:   # no duplication for ids should be added
                matching_route_ids.append(route_id)


    if not matching_route_ids:
        return []                    # no route connecting pickof and dropoff query

    now = datetime.utcnow()               # future trips on the routes which the user search

    available_trips = Trip.query.filter(
        Trip.route_id.in_(matching_route_ids),
        Trip.departure_time >= now,
        Trip.status == 'SCHEDULED'
    ).order_by(Trip.departure_time.asc()).all()

    
    results = []        # results
    for trip in available_trips:
        results.append(trip.to_dict())

    return results



def get_all_trips():
    
    trips = Trip.query.order_by(
        Trip.departure_time.desc()
    ).all()

    return [trip.to_dict() for trip in trips]



def update_trip_details(trip_id, data):

    trip = Trip.query.get(trip_id)
    
    if not trip:
        return None, 'trip not found'

    if 'status' in data:
        allowed_statuses = ['SCHEDULED', 'CANCELLED', 'COMPLETED', 'IN_PROGRESS']

        if data['status'] not in allowed_statuses:
            return None, f"invalid status. Must be one of: {', '.join(allowed_statuses) }"

        trip.status = data

    # handling possible update conflict, incase driver or vehicle was already assined at the same time
    new_driver_id = data.get('driver_id', trip.driver_id)
    new_vehicle_id = data.get('vehicle_id', trip.vehicle_id)
    new_time_str = data.get('departure_time')

    if new_time_str:    # fixing time conflict incase there be one
        try:
            new_time = datetime.fromisoformat(new_time_str)
        except ValueError:
            return None, "invalid date format, please use YYYY-MM-DDTHH:MM:SS"
    else:
        new_time = trip.departure_time

        # fixing driver conflict incase there be one, let's say if driver, vehicle or time is changing then we have to check to ensure it does not overlap with another trip which has already been scheduled
    if new_driver_id != trip.driver_id or new_vehicle_id != trip.vehicle_id or new_time != trip.departure_time:
        time_window_start = new_time - timedelta(hours = 1)
        time_window_end = new_time + timedelta(hours = 1)

        vehicle_conflict = Trip.query.filter(   # checkx vehicel conflix except for this trip
            Trip.vehicle_id == new_vehicle_id,
            Trip.id != trip.id, 
            Trip.departure_time >= time_window_start,
            Trip.departure_time <= time_window_end
        ).first()

        if vehicle_conflict:
            return None, "this vehicle has already been schedule for another trip around this time"

        driver_conflict = Trip.query.filter(  # checkx driver conflix except for this trip
            Trip.driver_id == new_driver_id,
            Trip.id != trip.id,
            Trip.departure_time >= time_window_start,
            Trip.departure_time <= time_window_end
        ).first()

        if driver_conflict:
            return None, "this driver has already been schedule for another trip around this time"

        
        trip.driver_id = new_driver_id
        trip.vehicle_id = new_vehicle_id
        trip.departure_time = new_time
    
    try:

        db.session.commit()

    except Exception as e:

        db.session.rollback()
        print('DB Error: ', e)
        return None, "DB error while updating trip"

    return trip, None



def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)
    
    if not trip:
        return False, "trip not found"

    try:

        db.session.delete(trip)
        db.session.commit()

    except Exception as e:

        db.session.rollback()

        return False, "DB error while deleting trip"

    return True, None
