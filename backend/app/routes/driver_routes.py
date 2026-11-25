
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required
from app.services.driver_service import create_new_driver, get_all_drivers, update_driver, delete_driver

driver_bp = Blueprint('driver', __name__, url_prefix = '/api/v1/drivers')

@driver_bp.route('/', methods = ['POST'])
@jwt_required()
@role_required('admin')
def add_driver():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "no data provided"
        }), 400

    driver, error = create_new_driver(data)

    if error:
        return jsonify({
            "error": error
        }), 400


    return jsonify({
        "message": "success creating driver",
        "driver": {
            "id": driver.id,
            "full_name": driver.full_name,
            "phone": driver.phone,
            "license_number": driver.license_number,
            "vehicle_id": driver.vehicle_id,
            "status": driver.status
        }
    }), 201

    
@driver_bp.route('/', methods = ['GET'])
@jwt_required()
@role_required('admin')
def get_drivers():

    drivers = get_all_drivers()

    return jsonify({
        "count": len(drivers),
        "drivers": drivers
    }), 200


@driver_bp.route('/<int:driver_id>', methods = ['PATCH'])
@jwt_required()
@role_required('admin')
def update_driver_route(driver_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "no update data provided"
        }), 400

    driver, error = update_driver(driver_id, data)
    if error:
        return jsonify({
            "error": error
        }), 400

    return jsonify({
        "message": "success updating driver",
        "driver": {
            "id": driver.id,
            "full_name": driver.full_name,
            "phone": driver.phone,
            "license_number": driver.license_number,
            "vehicle_id": driver.vehicle_id,
            "status": driver.status
        }
    }), 200


@driver_bp.route('/<int:driver_id>', methods = ['DELETE'])
@jwt_required()
@role_required('admin')
def delete_driver_route(driver_id):

    success, error = delete_driver(driver_id)

    if error:
        return jsonify({
            "error": error
        }), 404

    return jsonify({
        "message": "success deleting driver"
    }), 200

