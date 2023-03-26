from datetime import datetime
from models.db import db
from flask import request

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    manga_id=db.Column(db.Integer
                    #    , db.ForeignKey('manga.id', nullable=False)
                    )
    content=db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(
    ), nullable=False, onupdate=datetime.utcnow)
    user = db.relationship("User", back_populates="comments")

    def __init__(self, user_id, manga_id, content):
        self.user_id = user_id
        self.manga_id = manga_id
        self.content = content

    def json(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "manga_id": self.manga_id,
                "content": self.content}
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    #Find Methods
    @classmethod
    def find_all(cls):
        comments = Comment.query.all()
        return [c.json() for c in comments]
    
    @classmethod
    def find_by_id(cls, id):
        return db.get_or_404(cls, id, description = f'record with id: {id} is not available')
    
    @classmethod
    def find_by_manga_id(cls, manga_id):
        comments = cls.query.filter_by(manga_id=manga_id).all()
        return comments
    
    @classmethod
    def find_by_user_id(cls, user_id):
        comments = cls.query.filter_by(user_id=user_id).all()
        return comments
    
    @classmethod
    def find_by_user_id_manga_id(cls, user_id, manga_id):
        comments = cls.query.filter_by(user_id=user_id, manga_id=manga_id).all()
        return comments
    
    #UPDATE Methods
    def update(cls, id):
        comment = db.get_or_404(cls, id, description = f'Record with id:{id} is not available')
        data = request.get_json()
        comment.user_id = data['user_id']
        comment.manga_id = data['manga_id']
        comment.content = data['content']
        db.session.commit()
        return comment.json()
    
    #Delete Method
    def delete(cls, id):
        comment = db.get_or_404(cls, id, description = f'Record with id:{id} is not available')
        db.session.delete(comment)
        db.session.commit()
        return 'Deleted comment', 204