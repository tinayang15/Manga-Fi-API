from datetime import datetime
from models.db import db
from flask import request

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

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "created_at": str(self.created_at),
                "updated_at": str(self.updated_at)}
    
    #Create
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_all(cls):
        return User.query.all()
    
    #Get User By Id
    @classmethod
    def find_by_id(cls, id):
        return db.get_or_404(cls, id, description = f'Record with id: {id} is not available')
    
    @classmethod
    def delete(cls, id):
        user = db.get_or_404(cls, id, description = f'Record with id:{id} is not available')
        db.session.delete(user)
        db.session.commit()
        return 'Deleted User', 204
    
    @classmethod
    def update(cls, id):
        user = db.get_or_404(cls, id, description = f'Record with id:{id} is not available')
        data = request.get_json()
        user.email = data [ 'email']
        user.name = data ['name']
        user.password = data['password']
        user.image = data['image']
        db.session.commit()
        return user.json()