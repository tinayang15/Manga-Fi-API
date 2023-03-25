from models.db import db
from models.user_manga_list import User_Manga_List
from flask_restful import Resource
from flask import request

class User_Manga_Lists(Resource):
    def get(self):
        user_manga_lists = User_Manga_List.find_all()
        return user_manga_lists
    
    def post(self):
        data = request.get_json()
        params = {}
        for k in data.keys():
            params[k]=data[k]
        user_manga_list = User_Manga_List(**params)
        user_manga_list.create()
        return user_manga_list.json(), 201
    

class User_Manga_Lists_Details(Resource):
    def get(self, user_manga_list_id):
        pass

    def put(self, user_manga_list_id):
        data = request.get_json()
        user_manga_list = User_Manga_List.find_by_id(user_manga_list_id)
        for k in data.keys():
            user_manga_list[k]=data[k]
            db.session.commit()
            return user_manga_list.json()

