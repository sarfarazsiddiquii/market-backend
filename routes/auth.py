from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import Config
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    existing_user = Config.users_collection.find_one({'username': username})
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    hash_password = generate_password_hash(password)
    Config.users_collection.insert_one({'username': username, 'password': hash_password})
    return jsonify({"message": "Signup successful!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = Config.users_collection.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        # Generate JWT token
        access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
        return jsonify({
            "message": f"Welcome {username}!",
            "access_token": access_token
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"message": "Logged out successfully!"}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"username": current_user}), 200
