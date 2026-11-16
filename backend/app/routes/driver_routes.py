
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required
from app.services.driver_service import create_new_driver

driver_bp = Blueprint('driver', __name__, url_prefix = '/api/v1/drivers')

@driver_bp.route('/', methods = ['POST'])
@jwt_required()
@role_required('admin')
def add_driver():

    pass