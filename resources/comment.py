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
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return {'msg': 'comment not found'}, 404
        return comment.json(), 200
    
    def get(self, manga_id):
        comment = Comment.find_by_id(manga_id)
        if not comment:
            return {'msg': 'comment not found'}, 404
        return comment.json(), 200
    
    def get(self, user_id):
        comment = Comment.find_by_id(user_id)
        if not comment:
            return {'msg': 'comment not found'}, 404
        return comment.json(), 200
    
    def get(self, user_id, manga_id):
        comment = Comment.find_by_id(user_id, manga_id)
        if not comment:
            return {'msg': 'comment not found'}, 404
        return comment.json(), 200

    def put(self, comment_id):
        data = request.get_json()
        comment = Comment.find_by_id(comment_id)
        for k in data.keys():
            comment[k]=data[k]
            db.session.commit()
            return comment.json()
    
    def delete(self, comment_id):
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return {'msg': 'comment not found'}, 404
        db.session.delete(comment)
        db.session.commit()
        return {"msg": "comment deleted", "payload": comment_id}