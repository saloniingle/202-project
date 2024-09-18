import jwt
import os

#
from functools import wraps
from flask import request
#
from src.models.users import User

def login_required(roles):
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized",
                }, 401
            try:
                data = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
                current_user = User.query.filter_by(id=data["user_id"]).first()
                if current_user is None:
                    return {
                        "message": "Invalid Authentication token!",
                        "data": None,
                        "error": "Unauthorized",
                    }, 401
                if current_user.role.lower() not in roles:
                    return {
                        "message": "Unauthorized to access this route!",
                        "data": None,
                        "error": "Unauthorized",
                    }, 401
            except Exception as e:
                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": f"{str(e)} ",
                }, 500

            return f(*args, **kwargs)

        return decorated

    return token_required
