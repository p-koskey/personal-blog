from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
   
    
    # likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    # dislikes = db.relationship('PostDislike', backref='post', lazy='dynamic')

    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content= db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", foreign_keys=user_id)
  
    # comments = db.relationship('Comments', backref='title', lazy='dynamic')
    # likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    # dislikes = db.relationship('PostDislike', backref='post', lazy='dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls, category):
        posts = Post.query.filter_by(posttype=category).all()
        return posts
    
    @classmethod
    def get_all_posts(self):
        posts = Post.query.all()

        return posts

    @classmethod
    def get_post(cls, id):
        post = Post.query.filter_by(id=id).first()

        return post
    
    @classmethod
    def get_posts_by_user_id(cls, user_id):
        posts = Post.query.filter_by(user_id=user_id).first()
        user = User.query.filter_by(user_id = user_id)

        return posts

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),index = True)
    comments = db.Column(db.String(1000))
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, post):
        comments = Comments.query.filter_by(post_id=post).all()
        return comments