
from app.extensions import db
from app.models.vehicle import Vehicle


def create_new_vehicle(data):

    make = data.get('make')
    model = data.get('model')
    plate_number = data.get('plate_number')
    capacity = data.get('capacity')

    if not make or not model or not plate_number or not capacity:
        return None, "missing required fields data (make, model, plate_number, capacity)"

    existing_vehicle = Vehicle.query.filter_by(plate_number = plate_number).first()

    if existing_vehicle:
        return None, 'vehicle with this plate number already exists'

    new_vehicle = Vehicle(
        make = make,
        model = model,
        year = data.get('year'),
        plate_number = plate_number,
        capacity = int(capacity),
        status = "available"
    )

    try:

        db.session.add(new_vehicle)
        db.session.commit()

    except Exception as e:

        db.session.rollback()
        print("DB Error: ", e)
        
        return None, "Database error while creating vehicle"

    return new_vehicle, None

    pass
