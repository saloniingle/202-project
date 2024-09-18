from flask import Blueprint, jsonify, request

import jwt
import datetime
from dotenv import load_dotenv
import os
import hashlib

from src.models.users import User
from config import SERVER_ABS_PATH
from src.constants.errors import ErrorCostants

login_bp = Blueprint("Login", __name__)

def is_null_or_empty(field):
    if field is None or not str(field).strip():
        return True

    return False

# Function to generate JWT token
def generate_token(user_id, role):

    jwt_expiration_delta_str = os.getenv('JWT_EXPIRATION_DELTA_DAYS')
    
    if jwt_expiration_delta_str is None:
        raise ValueError("JWT_EXPIRATION_DELTA environment variable is not set.")
    
    jwt_expiration_delta = datetime.timedelta(days=int(jwt_expiration_delta_str))

    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.now(datetime.timezone.utc) + jwt_expiration_delta
    }
    token = jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    return token

# Function to generate hashed password
def generate_hashed_password(password):
    # Convert the password to bytes (required by hashlib)
    password_bytes = password.encode('utf-8')
    
    # Generate the SHA256 hash
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    
    return sha256_hash

@login_bp.route("/login", methods=['POST'])
def login():
    # Check if request contains JSON data
    if request.is_json:
        # Parse JSON data
        data = request.get_json()
        # Access data fields
        user_name = data.get('username')
        user_password = data.get('password')

        if is_null_or_empty(user_name):
            return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("user_name")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

        if is_null_or_empty(user_password):
            return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("user_password")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

        # Query the database for the user
        user = User.query.filter_by(username=user_name).first()

        hashed_password = generate_hashed_password(user_password)

        if user and (hashed_password == user.password_hash):
            # Generate JWT token
            token = generate_token(user.id, user.role)

            return jsonify({'token': token,
                            'user_type': user.role,
                            'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'notification': user.notification})  # Send token back as JSON response
        else:
            return jsonify({'error': 'Invalid username or password'}), 401  # Send error message and 401 status code
    else:
        return jsonify({"error": "Request body must be in JSON format"})

    