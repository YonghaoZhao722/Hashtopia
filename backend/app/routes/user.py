# backend/app/routes/user.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from app.extensions import db
from app.models.user import User
from app.models.post import Post

user_bp = Blueprint('user', __name__)

@user_bp.route('/users/profile/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    """Get user profile information by ID"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error fetching user profile: {str(e)}")
        return jsonify({'error': 'Failed to fetch user profile'}), 500

@user_bp.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Get user's posts by ID"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)

        user = User.query.get_or_404(user_id)
        posts = Post.query.filter_by(user_id=user_id) \
            .order_by(Post.created_at.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': posts.page
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching user posts: {str(e)}")
        return jsonify({'error': 'Failed to fetch user posts'}), 500

@user_bp.route('/users/<int:user_id>/liked-posts', methods=['GET'])
def get_liked_posts(user_id):
    """Get posts liked by user ID"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)

        user = User.query.get_or_404(user_id)
        liked_posts = user.liked_posts.order_by(Post.created_at.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'posts': [post.to_dict() for post in liked_posts.items],
            'total': liked_posts.total,
            'pages': liked_posts.pages,
            'current_page': liked_posts.page
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching liked posts: {str(e)}")
        return jsonify({'error': 'Failed to fetch liked posts'}), 500