
from app.extensions import db
from app.models.driver import Driver
from app.models.vehicle import Vehicle

def create_new_driver(data):

    full_name = data.get('full_name')
    phone = data.get('phone')
    email = data.get('email')
    password = data.get('password')
    license_number = data.get('license_number')
    vehicle_id = data.get('vehicle_id')

    if not full_name or not phone or not password or not license_number:
        return None, "missing required fields (full_name, phone, password, license_number)"

    if Driver.query.filter_by(
        phone = phone
    ).first():
        return None, "driver with this phone number already exist"
        
    if Driver.query.filter_by(
        license_number = license_number
    ).first():
        return None, "this license number is already registered"

    if vehicle_id:          # checkx if vehicle exist
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return None, "the assign vehicle ID does not exist"

    new_driver = Driver(
        full_name = full_name,
        phone = phone,
        email = email,
        license_number = license_number,
        vehicle_id = vehicle_id,
        status = "active" 
    )

    new_driver.set_password(password)

    try:

        db.session.add(new_driver)
        db.session.commit()

    except Exception as e:

        db.session.rollback()
        print("DB Error: ", e)
        return None, "database error while creating driver"

    return new_driver, None

    pass


