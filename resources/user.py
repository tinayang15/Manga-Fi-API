from flask import request
from flask_restful import Resource
from models.user import User
from models.db import db
from sqlalchemy.orm import joinedload

class Users(Resource):
    def get(self):
        users = User.find_all()
        return [u.json() for u in users]
    
    def post(self):
        data = request.get_json()
        user = User(**data)
        user.create()
        return user.json(), 201
    

class UserDetail(Resource):
    def get(self, user_id):
        user = User.query.options(joinedload('comments')).filter_by(id=user_id).first()
        comments = [t.json() for t in user.comments]
        return {**user.json(), 'comments': comments}
    