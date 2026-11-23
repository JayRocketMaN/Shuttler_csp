
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required
from app.services.bus_stop_service import create_new_bus_stop


bus_stop_bp = Blueprint('bus_stop', __name__, url_prefix = '/api/v1/bus-stops')

@bus_stop_bp.route('/', methods = ['POST'])
@jwt_required()
@role_required('admin')
def add_bus_stop():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "no data provided"
        }), 400

    stop, error = create_new_bus_stop(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    if not stop:
        return jsonify({
            "error": "unknown error ocured while creating bus stop"
        }), 500

    return jsonify({
        "message": "success creating Bus stop ",
        # "bus_stop":  stop.to_dict() 
        "bus_stop": {
            "id": stop.id,
            "name": stop.name,
            "address": stop.address,
            "latitude": stop.latitude,
            "longitude": stop.longitude,
            "is_active": stop.is_active
        }
    }), 201

    pass
