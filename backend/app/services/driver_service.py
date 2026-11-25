
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

    

def get_all_drivers():

    drivers = Driver.query.order_by(
        Driver.created_at.desc()
    ).all()

    result = []
    for d in drivers:
        result.append({
            "id": d.id,
            "full_name": d.full_name,
            "phone": d.phone,
            "email": d.email,
            "license_number": d.license_number,
            "vehicle_id": d.vehicle_id,
            "status": d.status
        })

    return result



def update_driver(driver_id, data):

    driver = Driver.query.get(driver_id)

    if not driver:
        return None, "driver not found"

    if 'full_name' in data:
        driver.full_name = data['full_name']

    if 'phone' in data:
        driver.phone = data['phone']

    if 'email' in data:
        driver.email = data['email']

    if 'license_number' in data:
        driver.license_number = data['license_number']

    if 'vehicle_id' in data:
        # checkx if vehicle exist
        if data['vehicle_id'] and not Vehicle.query.get( data['vehicle_id'] ):
            return None, 'assigne vehicle does not exist'
        
        driver.vehicle_id = data['vehicle_id']

    if 'status' in data:
        allowed_statuses = ['active', 'suspended', 'inactive']

        if data['status'] not in allowed_statuses:
            return None, f"invalid status, please let it be one of: {', '.join(allowed_statuses)}"
        
        driver.status = data['status']

    try:
        db.session.commit()
    except Exception as e:

        db.session.rollback()
        print("DB Error: ", e)
        return None, "DB error while updating driver"

    return driver, None


def delete_driver(driver_id):

    driver = Driver.query.get(driver_id)

    if not driver:
        return False, "driver not found"

    try:
        db.session.delete(driver)
        db.session.commit()
    except Exception as e:

        db.session.rollback()
        print("DB Error: ", e)
        return False, "DB error while deleting driver"

    return True, None
