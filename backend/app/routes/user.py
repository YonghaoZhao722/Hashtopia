# backend/app/routes/user.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from app.extensions import db
from app.models.user import User
from app.models.post import Post

user_bp = Blueprint('user', __name__)


@user_bp.route('/users/<username>', methods=['GET'])
def get_user_profile(username):
    """Get user profile information"""
    try:
        user = User.query.filter_by(username=username).first_or_404()
        return jsonify(user.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error fetching user profile: {str(e)}")
        return jsonify({'error': 'Failed to fetch user profile'}), 500


@user_bp.route('/users/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)

        data = request.get_json()

        # Update fields if provided
        if 'bio' in data:
            user.bio = data['bio']
        if 'gender' in data:
            user.gender = data['gender']
        if 'age' in data:
            user.age = data['age']
        if 'location' in data:
            user.location = data['location']

        db.session.commit()

        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        })
    except Exception as e:
        current_app.logger.error(f"Error updating profile: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500


@user_bp.route('/users/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """Upload user avatar"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)

        if 'avatar' not in request.files:
            return jsonify({'error': 'No avatar file provided'}), 400

        file = request.files['avatar']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(f"avatar_{current_user_id}_{file.filename}")
            upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars')
            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            # Update user avatar URL
            user.avatar = f"/uploads/avatars/{filename}"
            db.session.commit()

            return jsonify({
                'message': 'Avatar uploaded successfully',
                'avatar_url': user.avatar
            })
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    except Exception as e:
        current_app.logger.error(f"Error uploading avatar: {str(e)}")
        return jsonify({'error': 'Failed to upload avatar'}), 500


@user_bp.route('/users/<username>/posts', methods=['GET'])
def get_user_posts(username):
    """Get user's posts"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)

        user = User.query.filter_by(username=username).first_or_404()
        posts = Post.query.filter_by(user_id=user.id) \
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


@user_bp.route('/users/<username>/liked-posts', methods=['GET'])
def get_liked_posts(username):
    """Get posts liked by user"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)

        user = User.query.filter_by(username=username).first_or_404()
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


def allowed_file(filename):
    """Check if file type is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_bp.route('/users/<username>/follow', methods=['POST'])
@jwt_required()
def follow_user(username):
    """Follow a user"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)
        user_to_follow = User.query.filter_by(username=username).first_or_404()

        if current_user.id == user_to_follow.id:
            return jsonify({'error': 'Cannot follow yourself'}), 400

        current_user.follow(user_to_follow)

        return jsonify({
            'message': f'Successfully followed {username}',
            'followers_count': user_to_follow.followers_count
        })

    except Exception as e:
        current_app.logger.error(f"Error following user: {str(e)}")
        return jsonify({'error': 'Failed to follow user'}), 500


@user_bp.route('/users/<username>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_user(username):
    """Unfollow a user"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)
        user_to_unfollow = User.query.filter_by(username=username).first_or_404()

        current_user.unfollow(user_to_unfollow)

        return jsonify({
            'message': f'Successfully unfollowed {username}',
            'followers_count': user_to_unfollow.followers_count
        })

    except Exception as e:
        current_app.logger.error(f"Error unfollowing user: {str(e)}")
        return jsonify({'error': 'Failed to unfollow user'}), 500


@user_bp.route('/users/<username>/following', methods=['GET'])
def get_following(username):
    """Get list of users that this user follows"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        user = User.query.filter_by(username=username).first_or_404()
        following = user.following.paginate(
            page=page, per_page=per_page, error_out=False)

        return jsonify({
            'users': [user.to_dict() for user in following.items],
            'total': following.total,
            'pages': following.pages,
            'current_page': following.page
        })

    except Exception as e:
        current_app.logger.error(f"Error getting following list: {str(e)}")
        return jsonify({'error': 'Failed to get following list'}), 500


@user_bp.route('/users/<username>/followers', methods=['GET'])
def get_followers(username):
    """Get list of users following this user"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        user = User.query.filter_by(username=username).first_or_404()
        followers = user.followers.paginate(
            page=page, per_page=per_page, error_out=False)

        return jsonify({
            'users': [user.to_dict() for user in followers.items],
            'total': followers.total,
            'pages': followers.pages,
            'current_page': followers.page
        })

    except Exception as e:
        current_app.logger.error(f"Error getting followers list: {str(e)}")
        return jsonify({'error': 'Failed to get followers list'}), 500