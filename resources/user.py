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