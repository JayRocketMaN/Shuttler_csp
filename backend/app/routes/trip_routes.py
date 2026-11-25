
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required
from app.services.trip_service import create_new_trip, search_trips, get_all_trips, update_trip_details, delete_trip

trip_bp = Blueprint('trip', __name__, url_prefix = '/api/v1/trips')

@trip_bp.route('/', methods = ['POST'])
@jwt_required()
@role_required('admin')
def add_trip():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data provided"
        }), 400

    trip, error = create_new_trip(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    return jsonify({
        "message": "success scheduling trip",

        "trip": trip.to_dict()
    }), 201



@trip_bp.route('/search', methods = ['GET'])
def search_for_trips():

    pickup = request.args.get('pickup')
    dropoff = request.args.get('dropoff')

    if not pickup or not dropoff:
        return jsonify({
            "error": "please provide both 'pickup' and 'dropoff' query parameters locations"
        }), 400

    trips = search_trips(pickup, dropoff)

    return jsonify({
        "count": len(trips),
        "trips": trips
    }), 200


@trip_bp.route('/', methods = ['GET'])
@jwt_required()
@role_required('admin')
def get_trips():
    trips = get_all_trips()

    return jsonify({
        "count": len(trips),
        "trips": trips
    }), 200


@trip_bp.route('/<int:trip_id>', methods = ['PATCH'])
@jwt_required()
@role_required('admin')
def update_status(trip_id):

    data = request.get_json()
    if not data:
        return jsonify({
            "error": "no update data provided"
        }), 400


    trip, error = update_trip_details(trip_id, data)

    if error:
        return jsonify({
            "error": error
        }), 404 if "not found" in error else 400

    return jsonify({
        "message": "success updating trip",
        "trip": trip.to_dict()
    }), 200


@trip_bp.route('/<int:trip_id>', methods = ['DELETE'])
@jwt_required()
@role_required('admin')
def delete_trip_route(trip_id):

    success, error = delete_trip(trip_id)

    if error:
        return jsonify({
            "error": error
        }), 404

    return jsonify({
        "message": "trip deleted successfully"
    }), 200

