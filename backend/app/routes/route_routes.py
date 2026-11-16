
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required
from app.services.route_service import create_new_route


route_bp = Blueprint('route', __name__, url_prefix = '/api/v1/routes')

@route_bp.route('/', methods = ['POST'])
@jwt_required()
@role_required('admin')
def add_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "no data provided"
        }), 400

    new_route, error = create_new_route(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    return jsonify({
        "message": "success creating route",
        "route": new_route.to_dict()
    }), 201

    pass


