from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60),unique=True,  nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
