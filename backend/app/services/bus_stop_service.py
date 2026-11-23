
from app.extensions import db
from app.models.bus_stop import BusStop

def create_new_bus_stop(data):

    name = data.get('name')
    address = data.get('address')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not name or not address or not latitude or not longitude:
        return None, "missing required fields (name, address, latitude, longitude)"

    existing_stop = BusStop.query.filter_by(
        name = name
    ).first()

    if existing_stop:
        return None, "bus stop with this name already exist"

    new_stop = BusStop(
        name = name,
        address = address,
        latitude = float(latitude),
        longitude = float(longitude),
        is_active = True
    )

    try:

        db.session.add(new_stop)
        db.session.commit()

    except Exception as e:

        db.session.rollback()
        print("DB Error: ", e)

        return None, "database error while creating bus stop"

    return new_stop, None



