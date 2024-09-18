from flask import Blueprint, jsonify, request

from src.models.db import db
from src.models.users import User
from src.services.tokenManager import get_id_from_token
from src.constants.roles import RoleConstants
from src.constants.errors import ErrorCostants
from src.services.loginManager import login_required
from src.routes.courses import is_null_or_empty
from src.routes.login import generate_hashed_password

profile_bp = Blueprint("Profile", __name__, url_prefix="/profile")

@profile_bp.route("/", methods=['PUT'])
@login_required(roles=[RoleConstants.STUDENT, RoleConstants.ADMIN])
def update_profile():
    if not request.is_json:
        return jsonify({"error": ErrorCostants.JSON_REQUEST_BODY_REQUIRED["message"]}), ErrorCostants.JSON_REQUEST_BODY_REQUIRED["http_status_code"]

    data = request.get_json()
    username = data.get("username")
    notification = data.get("notification")
    firstname = data.get("firstname")
    lastname = data.get("lastname")

    if is_null_or_empty(username):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("username")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    if is_null_or_empty(firstname):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("firstname")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    if is_null_or_empty(lastname):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("lastname")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    if is_null_or_empty(notification):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("notification")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]

    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    user_profile = User.query.filter_by(id=user_id).first()
    if user_profile is None:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    existing_user = User.query.filter_by(username=username).first()
    if existing_user is not None and existing_user.id != user_id:
        return jsonify({"error": ErrorCostants.USER_ALREADY_EXISTS["message"].format(username)}), ErrorCostants.USER_ALREADY_EXISTS["http_status_code"]

    user_profile.first_name = firstname
    user_profile.last_name = lastname
    user_profile.username = username
    user_profile.notification = notification

    db.session.add(user_profile)
    db.session.commit()
    db.session.refresh(user_profile)

    profile_info = {
        'id': user_profile.id,
        'username': user_profile.username,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'role': user_profile.role,
        'notification': user_profile.notification
    }
    
    return jsonify(profile_info)

@profile_bp.route("", methods=['GET'])
@login_required(roles=[RoleConstants.ADMIN, RoleConstants.FACULTY, RoleConstants.STUDENT])
def get_profile():

    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]

    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    user_profile = User.query.filter_by(id=user_id).first()
    if user_profile is None:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    profile_info = {
        'id': user_profile.id,
        'username': user_profile.username,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'role': user_profile.role,
        'notification': user_profile.notification
    }

    return jsonify(profile_info)
