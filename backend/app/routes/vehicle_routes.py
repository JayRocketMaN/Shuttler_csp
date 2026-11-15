
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required
from app.services.vehicle_service import create_new_vehicle


vehicle_bp = Blueprint('vehicle', __name__, url_prefix = '/api/v1/vehicles')

@vehicle_bp.route('/', methods = ['POST'])
@jwt_required()
@role_required('admin')
def add_vehicle():

    pass



