from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from app.extensions import db
from app.models.user import User
from app.models.driver import Driver

auth_bp = Blueprint('auth', __name__, url_prefix = '/api/v1/auth')

@auth_bp.route('/register', methods = ['POST'])
def register():

    data = request.get_json()  # user data from postman/frontend

    if not data or not data.get('phone') or not data.get('password') or not data.get('full_name') or not data.get('email'):
        return jsonify({
            "error": "Missing required fields (full_name, phone, email, password)"
        }), 400

    phone = data.get('phone')
    email = data.get('email')
    role = data.get('role', 'user') # our default role

    # checking if user exist by phone or email in db
    user_exist_phone = User.query.filter_by(phone = phone).first()
    user_exist_email = User.query.filter_by(email = email).first()

    if user_exist_phone:
        return jsonify({
            "error": "A user with this phone number already exists"
        }) , 400

    if user_exist_email:
            return jsonify({
                "error": "A user with this email already exists"
            }) , 400

    new_user = User(
        full_name = data.get('full_name'),
        phone = phone,
        email = data.get('email'),
        role = role
    )

    new_user.set_password(data.get('password'))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "successfully registered user ",
        "user_id": new_user.id
    }), 201


@auth_bp.route('/login', methods = ['POST'])
def login():

    data = request.get_json()

    if not data or not data.get('phone') or not data.get('password'):
        return jsonify({
            "error": "Phone and password are needed"
        }), 400

    phone = data.get('phone')
    password = data.get('password')
    role = data.get('role', 'user') 

    # searchx for the user based on the role they occupy
    if role == 'driver':
        user = Driver.query.filter_by(phone = phone).first()

    else:  # both user n admin stored in the user table
        user = User.query.filter_by(phone = phone).first()

    if not user:
        return jsonify({
            "error": "Invalid phone number or password"
        }), 401

    if not user.check_password(password):
        return jsonify({
            "error": "Invalid phone number or password"
        }), 401

    additional_claims = {
        "role": role,
        'full_name': user.full_name
    }

    access_token = create_access_token(
        identity = str(user.id),
        additional_claims = additional_claims
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "role": role
    }), 200

@auth_bp.route('/profile', methods = ['GET'])
@jwt_required()
def get_profile():
    claims = get_jwt()
    user_id = claims.get('sub')

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "no user found"
        }), 400

    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role
    }), 200


# ==== TODO (After main Logic of app has been implemented) =======
# 0. making use of uuid, for now i'm using id
# 1. Set strong password validation rules after we have finished with the main functions of the project
# 2. OTP verification
# 3. Logout
# 4. Rate Limiting
# 5. Token refresh



    

