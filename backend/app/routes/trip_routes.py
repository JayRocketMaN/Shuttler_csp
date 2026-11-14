
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required
from app.services.trip_service import create_new_trip

trip_bp = Blueprint('trip', __name__, url_prefix = '/api/v1/trips')

@trip_bp.route('/', methods = ['POST'])
@jwt_required()
@role_required('admin')
def add_trip():
    pass

