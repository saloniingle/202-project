from flask import Blueprint, jsonify, request

from src.constants.roles import RoleConstants
from src.models.users import User
from src.constants.errors import ErrorCostants
from src.services.loginManager import login_required

faculty_bp = Blueprint("Faculty", __name__, url_prefix="/faculty")

@faculty_bp.route("/", methods=['GET'])
@login_required(roles=[RoleConstants.ADMIN])
def get_faculty_list():
    try:
        faculty_list = User.query.filter_by(role=RoleConstants.FACULTY).all()
        faculty_list_json = []
        for faculty in faculty_list:
            faculty_list_json.append({
                'id': faculty.id,
                'username': faculty.username,
                'first_name': faculty.first_name,
                'last_name': faculty.last_name,
            })
        return jsonify(faculty_list_json)
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]