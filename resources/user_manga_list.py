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
    
class UserMangaListByUserId(Resource):
    def get(self, user_id):
        user_manga_lists = User_Manga_List.find_by_user_id(user_id)
        if not user_manga_lists:
            return {'msg': 'user_manga_list not found'}, 404
        return [um.json() for um in user_manga_lists], 200
    
class UserMangaListByMangaId(Resource):
    def get(self, manga_id):
        user_manga_list = User_Manga_List.find_by_manga_id(manga_id)
        if not user_manga_list:
            return {'msg': 'user_manga_list not found'}, 404
        return [um.json() for um in user_manga_list], 200
    
class UserMangaListByUserIdMangaId(Resource):
    def get(self, user_id, manga_id):
        user_manga_lists = User_Manga_List.find_by_user_id_manga_id(user_id, manga_id)
        if not user_manga_lists:
            return {'msg': 'user_manga_list not found'}, 404
        return [um.json() for um in user_manga_lists], 200

class User_Manga_List_Detail(Resource):
    def get(self, user_manga_list_id):
        user_manga_list = User_Manga_List.find_by_id(user_manga_list_id)
        if not user_manga_list:
            return {'msg': 'user_manga_list not found'}, 404
        return user_manga_list.json(), 200

    def put(self, user_manga_list_id):
        data = request.get_json()
        user_manga_list = User_Manga_List.find_by_id(user_manga_list_id)
        if not user_manga_list:
            return{'msg': 'user_manga_list not found'}, 404
        user_id = data.get('user_id')
        manga_id = data.get('manga_id')
        if user_id:
            user_manga_list.user_id = user_id
        if manga_id:
            user_manga_list.manga_id=manga_id
        db.session.commit()
        return user_manga_list.json()
        
    def delete(self, user_manga_list_id):
        user_manga_list = User_Manga_List.find_by_id(user_manga_list_id)
        if not user_manga_list:
            return {'msg': 'user_manga_list not found'}, 404
        db.session.delete(user_manga_list)
        db.session.commit()
        return {"msg": "user_manga_list deleted", "payload": user_manga_list_id}
