# backend/app/models/user.py
from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Profile information
    avatar = db.Column(db.String(200))
    bio = db.Column(db.Text)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Remove the duplicate posts relationship, it will be defined in Post model
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Keep the likes relationship
    liked_posts = db.relationship(
        'Post',
        secondary='post_likes',
        backref=db.backref('liked_by', lazy='dynamic'),
        lazy='dynamic'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'bio': self.bio,
            'gender': self.gender,
            'age': self.age,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Post likes association table
post_likes = db.Table('post_likes',
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                      db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
                      db.Column('created_at', db.DateTime, default=datetime.utcnow)
                      )