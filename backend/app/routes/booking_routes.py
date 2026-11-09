
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.booking_service import create_new_booking, get_user_bookings


booking_bp = Blueprint('booking', __name__, url_prefix = '/api/v1/bookings')

@booking_bp.route('/', methods = ['POST'])
@jwt_required()
def book_trip():

    current_user_id = get_jwt_identity()

    data = request.get_json()

    if not data or not data.get('trip_id'):
        return jsonify({
            "error": "The trip ID is required"
        }), 400

    booking, error = create_new_booking(current_user_id, data)

    if error:
        return jsonify({
            "error": error
        }), 400


    return jsonify({
        "message": "Booking created successfully",
        "booking": {
            "id": booking.id,
            "trip_id": booking.trip_id,
            "pickup": booking.pickup_location,
            "dropoff": booking.dropoff_location,
            "seats": booking.seat_count,
            "total_amount": str(booking.total_amount),
            "status": booking.status
        }
    }), 201


@booking_bp.route('/', methods = ['GET'])
@jwt_required()
def get_my_bookings():
    
    current_user_id = int(get_jwt_identity())
    
    my_bookings = get_user_bookings(current_user_id)

    
    return jsonify({
        "count": len(my_bookings),
        "bookings": my_bookings
    }), 200

