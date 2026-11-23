
from app.extensions import db
from app.models.route import Route, RouteStop
from app.models.bus_stop import BusStop


# ========== This service those the ff 2 things: 
    # - It creates the Route & then loops through the stop_ids which the admin provides and creates the RouteStop records

def create_new_route(data):

    name = data.get('name')
    description = data.get('description')
    stop_ids = data.get('stop_ids')  # list: [1, 2, 3, ....]

    if not name or not stop_ids:
        return None, "missing required fields (name, stop_ids)"

    if not isinstance(stop_ids, list) or len(stop_ids) < 2:
        return None, "a route must have at least 2 bus stops. e.g [1, 2, etc]"

    if Route.query.filter_by(     # checkx if name exist
        name = name
    ).first():
        
        return None, "a route with this name already exist"

    for stop_id in stop_ids:      # verifying if all stops actually exist

        if not BusStop.query.get(stop_id):

            return None, f"bus stop with ID {stop_id} does not exist"

    new_route = Route(
        name = name,
        description = description,
        is_active = True
    )

    try: 
        db.session.add(new_route)
        db.session.flush()         # getting the new route id before commiting

        for index, stop_id in enumerate(stop_ids):   # looping through the stop_ids to link them to the route in order

            route_stop = RouteStop(
                route_id = new_route.id,
                bus_stop_id = stop_id,
                stop_order = index + 1 # order: 1, 2, 3, ......, with 1 being the bus_start location and last number being the final bus_stop location
            )

            db.session.add(route_stop)

        db.session.commit()

    except Exception as e:

        db.session.rollback()
        print("============= DB ERROR ===========")
        print(e) 
        print("================================")

        return None, "database error while creating route"

    return new_route, None




