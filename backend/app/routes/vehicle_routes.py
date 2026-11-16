
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required
from app.services.vehicle_service import create_new_vehicle


vehicle_bp = Blueprint('vehicle', __name__, url_prefix = '/api/v1/vehicles')

@vehicle_bp.route('/', methods = ['POST'])
@jwt_required()
@role_required('admin')
def add_vehicle():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "no data provided"
        }), 400

    vehicle, error = create_new_vehicle(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    return jsonify({
        "message": "success adding Vehicle",
        "vehicle": {
            "id": vehicle.id,
            "make": vehicle.make,
            "model": vehicle.model,
            "plate_number": vehicle.plate_number,
            "capacity": vehicle.capacity,
            "status": vehicle.status
        }
    }), 201


    pass



