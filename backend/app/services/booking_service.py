from datetime import datetime

from app.extensions import db
from app.models.booking import Booking
from app.models.trip import Trip

# promo code will be added after, this is just a flat rate
FARE_PER_SEAT = 1500 
INSURANCE_FEE = 100


def create_new_booking(user_id, data):
    
    trip_id = data.get('trip_id')
    trip = Trip.query.get(trip_id)
    
    if not trip: # checking if the trip exists
        return None, 'Trip not found'

    
    seats = int(data.get('seat_count', 1))
    pickup = data.get('pickup_location')
    dropoff = data.get('dropoff_location')

    if not pickup or not dropoff:
        return None, 'the pickup and dropoff locations are required'

    
    total_amount = (FARE_PER_SEAT * seats) + INSURANCE_FEE

    
    new_booking = Booking(
        user_id = user_id,
        trip_id = trip_id,
        pickup_location = pickup,
        dropoff_location = dropoff,
        seat_count = seats,
        total_amount = total_amount,
        status = "pending_payment"
    )

    
    try:
        db.session.add(new_booking)
        db.session.commit()

    except Exception as e:

        db.session.rollback()
        print('db error: ', e)
        return None, 'database error while creating booking'

    return new_booking, None

