from datetime import datetime
from models.db import db
from flask import request

class User_Manga_List(db.Model):
    __tablename__ = 'user_manga_lists'

    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    manga_id=db.Column(db.Integer
                    #    , db.ForeignKey('manga.id', nullable=False)
                    )
    favorite_list=db.Column(db.ARRAY(db.String))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(
    ), nullable=False, onupdate=datetime.utcnow)
    user = db.relationship("User", back_populates="user_manga_lists")
    # manga = db.relationship("Manga", back_populates="user_manga_lists")

    def __init__(self, user_id, manga_id, favorite_list):
        self.user_id = user_id
        self.manga_id = manga_id
        self.favorite_list = favorite_list

    def json(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "manga_id": self.manga_id,
                "favorite_list": self.favorite_list}
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    #FIND Methods
    @classmethod
    def find_all(cls):
        user_manga_lists = User_Manga_List.query.all()
        return [u.json() for u in user_manga_lists]
    
    @classmethod
    def find_by_id(cls, id):
        return db.get_or_404(cls, id, description = f'record with id: {id} is not available')
    
    @classmethod
    def find_by_manga_id(cls, manga_id):
        user_manga_lists = cls.query.filter_by(manga_id=manga_id).all()
        return user_manga_lists
    
        # def find_all_by_user_id(cls, user_id):
        # return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def find_by_user_id(cls, user_id):
        user_manga_lists = cls.query.filter_by(user_id=user_id).all()
        return user_manga_lists
    
    @classmethod
    def find_by_user_id_manga_id(cls, user_id, manga_id):
        user_manga_lists = cls.query.filter_by(user_id=user_id, manga_id=manga_id).all()
        return user_manga_lists
    
    #UPDATE Methods
    def update(cls, id):
        user_manga_list = db.get_or_404(cls, id, description = f'Record with id:{id} is not available')
        data = request.get_json()
        user_manga_list.user_id = data['user_id']
        user_manga_list.manga_id = data['manga_id']
        user_manga_list.favorite_list = data['favorite_list']
        db.session.commit()
        return user_manga_list.json()
    
    #Delete Method
    def delete(cls, id):
        user_manga_list = db.get_or_404(cls, id, description = f'Record with id:{id} is not available')
        db.session.delete(user_manga_list)
        db.session.commit()
        return 'Deleted user_manga_list', 204

    