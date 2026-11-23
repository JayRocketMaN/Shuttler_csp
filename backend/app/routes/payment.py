import hashlib
import hmac
import json
import os
from decimal import Decimal, InvalidOperation
from uuid import uuid4

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.extensions import db
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.trip import Trip
from app.models.user import User


payment_bp = Blueprint('payment', __name__, url_prefix='/api/v1/payments')


# Initializes a Paystack transaction and returns its authorization URL.
def paystack_initialize(email, amount_kobo, reference):
    try:
        import requests
    except ImportError:
        return None

    try:
        secret_key = os.environ['PAYSTACK_SECRET_KEY']
        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            headers={'Authorization': f'Bearer {secret_key}'},
            json={
                'email': email,
                'amount': amount_kobo,
                'reference': reference,
            },
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()
    except (KeyError, requests.RequestException, ValueError):
        return None

    if not isinstance(result, dict) or not result.get('status'):
        return None
    return (result.get('data') or {}).get('authorization_url')


# Requests a refund for a Paystack transaction reference.
def paystack_refund(reference):
    try:
        import requests
    except ImportError:
        return False

    try:
        secret_key = os.environ['PAYSTACK_SECRET_KEY']
        response = requests.post(
            'https://api.paystack.co/refund',
            headers={'Authorization': f'Bearer {secret_key}'},
            json={'transaction': reference},
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()
    except (KeyError, requests.RequestException, ValueError):
        return False

    return isinstance(result, dict) and bool(result.get('status'))


# Returns the logged-in user's integer ID from the JWT identity.
def _current_user_id():
    try:
        return int(get_jwt_identity())
    except (TypeError, ValueError):
        return None


# Checks whether the logged-in JWT contains the admin role.
def _is_admin():
    return get_jwt().get('role') == 'admin'


# Initializes payment for an owned pending booking.
@payment_bp.route('/initiate', methods=['POST'])
@jwt_required()
def initiate_payment():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'A JSON object is required'}), 400

    booking_id = data.get('booking_id')
    if isinstance(booking_id, bool) or not isinstance(booking_id, int):
        return jsonify({'error': 'booking_id must be an integer'}), 400

    user_id = _current_user_id()
    if user_id is None:
        return jsonify({'error': 'Invalid JWT identity'}), 401

    booking = db.session.get(Booking, booking_id)
    if booking is None:
        return jsonify({'error': 'Booking not found'}), 404
    if booking.user_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403
    if booking.status != 'pending':
        return jsonify({'error': 'Booking is not pending'}), 409
    if not hasattr(Booking, 'total_amount'):
        return jsonify({'error': 'Booking model is missing total_amount'}), 409

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    if not user.email:
        return jsonify({'error': 'User email is required for payment'}), 409

    try:
        amount_kobo = int(Decimal(str(booking.total_amount)) * Decimal('100'))
    except (InvalidOperation, TypeError, ValueError):
        return jsonify({'error': 'Booking amount is invalid'}), 409

    reference = f'shuttler-{uuid4().hex}'
    authorization_url = paystack_initialize(user.email, amount_kobo, reference)
    if not authorization_url:
        return jsonify({'error': 'Could not initialize payment'}), 502

    payment = Payment(
        booking_id=booking.id,
        user_id=user_id,
        reference=reference,
        transaction_reference=reference,
        amount=booking.total_amount,
        status='pending',
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({
        'payment': payment.to_dict(),
        'authorization_url': authorization_url,
    }), 201


# Verifies Paystack's signature and confirms a successful payment idempotently.
@payment_bp.route('/webhook', methods=['POST'])
def paystack_webhook():
    try:
        secret_key = os.environ['PAYSTACK_SECRET_KEY']
    except KeyError:
        return jsonify({'error': 'Paystack is not configured'}), 500

    raw_body = request.get_data(cache=True)
    signature = request.headers.get('x-paystack-signature', '')
    expected_signature = hmac.new(
        secret_key.encode('utf-8'),
        raw_body,
        hashlib.sha512,
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        return jsonify({'error': 'Invalid Paystack signature'}), 401

    try:
        payload = json.loads(raw_body)
    except (TypeError, ValueError):
        return jsonify({'status': 'ignored'}), 200
    if not isinstance(payload, dict) or payload.get('event') != 'charge.success':
        return jsonify({'status': 'ignored'}), 200

    event_data = payload.get('data') or {}
    reference = event_data.get('reference') if isinstance(event_data, dict) else None
    if not reference:
        return jsonify({'status': 'ignored'}), 200

    payment = Payment.query.filter_by(reference=reference).first()
    if payment is None or payment.status != 'pending':
        return jsonify({'status': 'ignored'}), 200

    booking = db.session.get(Booking, payment.booking_id)
    if booking is None or not hasattr(Booking, 'seat_count'):
        return jsonify({'status': 'ignored'}), 200

    updated_rows = Trip.query.filter(
        Trip.id == booking.trip_id,
        Trip.booked_count + booking.seat_count <= Trip.capacity,
    ).update(
        {'booked_count': Trip.booked_count + booking.seat_count},
        synchronize_session=False,
    )

    if updated_rows:
        payment.status = 'success'
        booking.status = 'confirmed'
        # TODO: create notification
    else:
        payment.status = 'refunded'
        booking.status = 'failed'
        paystack_refund(reference)
        # TODO: create notification

    db.session.commit()
    return jsonify({'status': 'processed'}), 200


# Returns a payment only to its booking owner or an administrator.
@payment_bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id):
    user_id = _current_user_id()
    if user_id is None:
        return jsonify({'error': 'Invalid JWT identity'}), 401

    payment = db.session.get(Payment, payment_id)
    if payment is None:
        return jsonify({'error': 'Payment not found'}), 404

    booking = db.session.get(Booking, payment.booking_id)
    if booking is None:
        return jsonify({'error': 'Booking not found'}), 404
    if booking.user_id != user_id and not _is_admin():
        return jsonify({'error': 'Forbidden'}), 403
    return jsonify(payment.to_dict()), 200
