# backend/app/routes/auth.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        current_app.logger.info(f"Received registration request: {data}")

        # Validate required fields
        required_fields = ['email', 'username', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 400

        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )

        db.session.add(user)
        db.session.commit()

        # Create token
        token = create_access_token(identity=user.id)

        current_app.logger.info(f"Successfully registered user: {user.username}")

        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    except Exception as e:
        current_app.logger.error(f"Error during registration: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Server error during registration'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400

        # Find user by username
        user = User.query.filter_by(username=data['username']).first()

        # Verify user and password
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401

        # Create token
        token = create_access_token(identity=user.id)

        current_app.logger.info(f"User logged in successfully: {user.username}")

        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    except Exception as e:
        current_app.logger.error(f"Error during login: {str(e)}")
        return jsonify({'error': 'Server error during login'}), 500


@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify JWT token and return user data"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    except Exception as e:
        current_app.logger.error(f"Error verifying token: {str(e)}")
        return jsonify({'error': 'Server error during token verification'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching profile: {str(e)}")
        return jsonify({'error': 'Server error while fetching profile'}), 500