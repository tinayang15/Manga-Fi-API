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
    
    