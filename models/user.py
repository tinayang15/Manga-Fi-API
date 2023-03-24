from datetime import datetime
from models.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=str(
        datetime.utcnow()), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(
    ), nullable=False, onupdate=datetime.now())
    comments = db.relationship("Comment", cascade="all", back_populates="user")
    user_manga_lists = db.relationship("User_Manga_List", cascade="all", back_populates="user")

    def __init__(self, name, email, password, image):
        self.name = name
        self.email = email
        self.password = password
        self.image = image