from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from app.services.auth_service import create_user, authenticate_user
from flask_jwt_extended import create_access_token, jwt_required

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    result = create_user(data)
    return jsonify(result), result['status']
    
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    result = authenticate_user(data)
    return jsonify(result), result['status']

@auth_bp.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"msg": "Logout successful"}), 200
