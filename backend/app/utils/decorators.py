
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(required_role):
    def wrapper(fn):

        @wraps(fn)
        def decorator(*args, **kwargs):

            verify_jwt_in_request()  # checkx if the token send by the user is valid

            claims = get_jwt()
            user_role = claims.get("role")  # extractx role from the token claims

            if user_role != required_role:
                return jsonify({
                    "error": "You don't have permission to access here"
                })

            return fn(*args, **kwargs) # the route runs if the users role matches the required role

        return decorator

    return wrapper