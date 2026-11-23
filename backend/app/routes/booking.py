from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.extensions import db
from app.models.booking import Booking
from app.models.trip import Trip
from app.models.user import User


booking_bp = Blueprint('booking', __name__, url_prefix='/api/v1/bookings')


# Returns the logged-in user's integer ID from the JWT identity.
def _current_user_id():
    try:
        return int(get_jwt_identity())
    except (TypeError, ValueError):
        return None


# Checks whether the logged-in JWT contains the admin role.
def _is_admin():
    return get_jwt().get('role') == 'admin'


# Creates a pending booking after validating its trip and seat count.
@booking_bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'A JSON object is required'}), 400

    trip_id = data.get('trip_id')
    pickup_location = data.get('pickup_location')
    dropoff_location = data.get('dropoff_location')
    seat_count = data.get('seat_count', 1)

    if isinstance(trip_id, bool) or not isinstance(trip_id, int):
        return jsonify({'error': 'trip_id must be an integer'}), 400
    if not isinstance(pickup_location, str) or not pickup_location.strip():
        return jsonify({'error': 'pickup_location is required'}), 400
    if not isinstance(dropoff_location, str) or not dropoff_location.strip():
        return jsonify({'error': 'dropoff_location is required'}), 400
    if isinstance(seat_count, bool) or not isinstance(seat_count, int) or seat_count < 1:
        return jsonify({'error': 'seat_count must be an integer greater than or equal to 1'}), 400

    user_id = _current_user_id()
    if user_id is None:
        return jsonify({'error': 'Invalid JWT identity'}), 401
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    trip = db.session.get(Trip, trip_id)
    if trip is None:
        return jsonify({'error': 'Trip not found'}), 404
    if trip.status != 'scheduled':
        return jsonify({'error': 'Trip is not scheduled'}), 409

    capacity = trip.capacity
    booked_count = trip.booked_count or 0
    if capacity is None or capacity - booked_count < seat_count:
        return jsonify({'error': 'Not enough seats'}), 409
    if trip.price is None:
        return jsonify({'error': 'Trip price is unavailable'}), 409

    required_fields = ('pickup_location', 'dropoff_location', 'seat_count', 'total_amount')
    if any(not hasattr(Booking, field) for field in required_fields):
        return jsonify({'error': 'Booking model is missing multi-seat fields'}), 409

    try:
        total_amount = Decimal(str(trip.price)) * Decimal(seat_count)
    except (InvalidOperation, TypeError, ValueError):
        return jsonify({'error': 'Trip price is invalid'}), 409

    booking = Booking(
        user_id=user_id,
        trip_id=trip.id,
        pickup_location=pickup_location.strip(),
        dropoff_location=dropoff_location.strip(),
        seat_count=seat_count,
        total_amount=total_amount,
        status='pending',
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking.to_dict()), 201


# Lists only the current passenger's bookings, or an admin's requested user.
@booking_bp.route('', methods=['GET'])
@jwt_required()
def list_bookings():
    user_id = _current_user_id()
    if user_id is None:
        return jsonify({'error': 'Invalid JWT identity'}), 401

    if _is_admin():
        requested_user_id = request.args.get('user_id')
        if requested_user_id is not None:
            try:
                user_id = int(requested_user_id)
            except ValueError:
                return jsonify({'error': 'user_id must be an integer'}), 400

    bookings = (
        Booking.query.filter_by(user_id=user_id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return jsonify({'items': [booking.to_dict() for booking in bookings]}), 200


# Returns one booking only to its owner or an administrator.
@booking_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    user_id = _current_user_id()
    if user_id is None:
        return jsonify({'error': 'Invalid JWT identity'}), 401

    booking = db.session.get(Booking, booking_id)
    if booking is None:
        return jsonify({'error': 'Booking not found'}), 404
    if booking.user_id != user_id and not _is_admin():
        return jsonify({'error': 'Forbidden'}), 403
    return jsonify(booking.to_dict()), 200


# Soft-cancels a booking and releases seats only if it was confirmed.
@booking_bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    user_id = _current_user_id()
    if user_id is None:
        return jsonify({'error': 'Invalid JWT identity'}), 401

    booking = db.session.get(Booking, booking_id)
    if booking is None:
        return jsonify({'error': 'Booking not found'}), 404
    if booking.user_id != user_id and not _is_admin():
        return jsonify({'error': 'Forbidden'}), 403
    if booking.status in ('cancelled', 'failed'):
        return jsonify({'error': 'Booking cannot be cancelled'}), 409
    if booking.status not in ('pending', 'confirmed'):
        return jsonify({'error': 'Booking cannot be cancelled'}), 409

    if booking.status == 'confirmed':
        if not hasattr(Booking, 'seat_count'):
            return jsonify({'error': 'Booking model is missing seat_count'}), 409
        trip = db.session.get(Trip, booking.trip_id)
        if trip is None:
            return jsonify({'error': 'Trip not found'}), 404
        Trip.query.filter(Trip.id == booking.trip_id).update(
            {'booked_count': Trip.booked_count - booking.seat_count},
            synchronize_session=False,
        )
        # TODO: refund a confirmed booking through the payment provider

    booking.status = 'cancelled'
    db.session.commit()
    return jsonify(booking.to_dict()), 200
