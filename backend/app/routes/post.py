# backend/app/routes/post.py
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.post import Post, PostImage, Tag

# Create blueprint with a custom prefix that matches the registration in __init__.py
post_bp = Blueprint('post', __name__, url_prefix='/api/posts')

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    """
    Create a new post with images and tags
    Requires authentication
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags', '[]')
        
        # Validate required fields
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400
        
        # Create new post
        post = Post(
            title=title,
            content=content,
            user_id=current_user_id
        )
        
        # Process tags
        try:
            import json
            tag_names = json.loads(tags)
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                post.tags.append(tag)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid tags format'}), 400
        
        # Process images
        if 'images' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
            
        files = request.files.getlist('images')
        image_urls = []
        
        for file in files:
            if file and allowed_file(file.filename):
                # Generate secure unique filename
                filename = secure_filename(file.filename)
                unique_filename = f"{current_user_id}_{int(datetime.utcnow().timestamp())}_{filename}"
                
                # Ensure upload directory exists
                upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Save file
                file_path = os.path.join(upload_folder, unique_filename)
                file.save(file_path)
                
                # Create image record
                image = PostImage(
                    url=f"/uploads/posts/{unique_filename}",
                    post=post
                )
                db.session.add(image)
                image_urls.append(image.url)
        
        # Save everything to database
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': post.to_dict()
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error creating post: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Server error while creating post'}), 500

@post_bp.route('/', methods=['GET'])
def get_posts():
    """
    Get paginated list of posts
    Optional query parameters: page, per_page
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get posts with pagination
        posts = Post.query.order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': posts.page
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching posts: {str(e)}")
        return jsonify({'error': 'Server error while fetching posts'}), 500

@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post by its ID"""
    try:
        post = Post.query.get_or_404(post_id)
        return jsonify(post.to_dict())
        
    except Exception as e:
        current_app.logger.error(f"Error fetching post {post_id}: {str(e)}")
        return jsonify({'error': 'Server error while fetching post'}), 500