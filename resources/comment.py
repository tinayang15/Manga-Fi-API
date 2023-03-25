from models.db import db
from models.comment import Comment
from flask_restful import Resource
from flask import request

class Comments(Resource):
    def get(self):
        comments = Comment.find_all()
        return comments
    
    def post(self):
        data = request.get_json()
        params = {}
        for k in data.keys():
            params[k]=data[k]
        comment = Comment(**params)
        comment.create()
        return comment.json(), 201
    
class CommentDetail(Resource):
    def get(self, comment_id):
        pass

    def put(self, comment_id):
        data = request.get_json()
        comment = Comment.find_by_id(comment_id)
        for k in data.keys():
            comment[k]=data[k]
            db.session.commit()
            return comment.json()