from datetime import datetime
from models.db import db
from flask import request

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id', nullable=False))
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