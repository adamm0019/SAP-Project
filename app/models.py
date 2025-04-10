from datetime import datetime
import bleach
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    messages = db.relationship('Message', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    sanitized_body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Message {self.id}>'

    def set_body(self, body):
        self.body = body
        allowed_tags = ['b', 'i', 'u', 'p', 'br', 'ul', 'ol', 'li', 'strong', 'em']
        self.sanitized_body = bleach.clean(body, tags=allowed_tags, strip=True)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))