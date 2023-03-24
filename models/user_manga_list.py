from datetime import datetime
from models.db import db

class User_Manga_List(db.model):
    __tablename__ = 'user_manga_lists'

    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id', nullable=False))
    manga_id=db.Column(db.Integer
                    #    , db.ForeignKey('manga.id', nullable=False)
                    )
    favorite_list=db.Column(db.Array)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(
    ), nullable=False, onupdate=datetime.utcnow)
    user = db.relationship("User", back_populates="user_manga_lists")
    # manga = db.relationship("Manga", back_populates="user_manga_lists")

    def __init__(self, user_id, manga_id, favorite_list):
        self.user_id = user_id
        self.manga_id = manga_id
        self.favorite_list = favorite_list