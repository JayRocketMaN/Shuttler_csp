
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


def get_all_vehicles():

    vehicles = Vehicle.query.order_by(
        Vehicle.created_at.desc()
    ).all()

    return [{
        "id": v.id,
        "make": v.make,
        "model": v.model,
        "year": v.year,
        "plate_number": v.plate_number,
        "capacity": v.capacity,
        "status": v.status
    } for v in vehicles]



def update_vehicle(vehicle_id, data):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return None, "vehicle not found"

    if 'make' in data:
        vehicle.make = data['make']

    if 'model' in data:
        vehicle.model = data['model']

    if 'year' in data:
        vehicle.year = data['year']

    if 'plate_number' in data:
        vehicle.plate_number = data['plate_number']

    if 'capacity' in data:
        vehicle.capacity = int(data['capacity'])

    if 'status' in data:
        allowed_statuses = ['available', 'maintenance', 'out_of_service']

        if data['status'] not in allowed_statuses:

            return None, f"invalid status, let it be one of: {', '.join(allowed_statuses)}"
        
        vehicle.status = data['status']


    try:

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('DB Error: ', e)

        return None, 'DB error while updating vehicle'

    return vehicle, None


def delete_vehicle(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return False, 'vehicle not found'

    try:

        db.session.delete(vehicle)
        db.session.commit()

    except Exception as e:

        db.session.rollback()
        print('DB Error: ', e)

        return False, "DB error while deleting vehicle"

    return True, None 

