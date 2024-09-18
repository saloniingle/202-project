from flask import Blueprint, request, jsonify

from src.services.loginManager import login_required

logout_bp = Blueprint("Logout", __name__)

@logout_bp.route("/logout", methods=['POST'])
@login_required(roles=["admin", "faculty", "student"])
def logout():
    return jsonify({'logout_status': 'logout successful'})  # Send logout successful
    
    