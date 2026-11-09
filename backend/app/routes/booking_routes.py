
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.booking_service import create_new_booking


booking_bp = Blueprint('booking', __name__, url_prefix='/api/v1/bookings')

@booking_bp.route('/', methods=['POST'])
@jwt_required()
def book_trip():

    pass

