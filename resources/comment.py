from models.db import db
from models.comment import Comment
from flask_restful import Resource
from flask import request

class Comments(Resource):
    def get(self):
        comments = Comment.find_all()
        return comments
    