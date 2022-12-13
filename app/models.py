from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.ext.mutable import MutableSet

class followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Followers {}>'.format(self.body)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.Column(MutableSet.as_mutable(db.PickleType))
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if self.followed is None:
            self.followed = MutableSet({user.id})
        elif not self.is_following(user):
            self.followed.add(user.id)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user.id)

    def is_following(self, user):
        if self.followed is None:
            return False
        return user.id in self.followed

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def incLikes(self):
        if self.likes is None:
            self.likes = 1
        else:
            self.likes = self.likes + 1

    def incDislikes(self):
        if self.dislikes is None:
            self.dislikes = 1
        else:
            self.dislikes = self.dislikes + 1
