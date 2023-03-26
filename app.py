from flask import Flask, render_template
import urllib.request, json
import os
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from models.db import db
from models import user, user_manga_list, comment
from resources import user, user_manga_list, comment

app = Flask(__name__)
CORS(app)
api = Api (app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/manga_fi"
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
migrate = Migrate(app,db)

api.add_resource(user.Users, '/users')
api.add_resource(user.UserDetail, '/users/<int:user_id>')
api.add_resource(user.UserDetailComments, '/users/comments/<int:user_id>')

api.add_resource(user_manga_list.User_Manga_Lists, '/user_manga_lists')
api.add_resource(user_manga_list.User_Manga_List_Detail, '/user_manga_lists/<int:user_manga_list_id>')
api.add_resource(user_manga_list.UserMangaListByUserId, '/user_manga_lists/user/<int:user_id>')
api.add_resource(user_manga_list.UserMangaListByMangaId, '/user_manga_lists/manga/<int:manga_id>')
api.add_resource(user_manga_list.UserMangaListByUserIdMangaId, '/user_manga_lists/user/<int:user_id>/manga/<int:manga_id>')

api.add_resource(comment.Comments, '/comments')
api.add_resource(comment.CommentDetail, '/comments/<int:comment_id>')
api.add_resource(comment.CommentByUserId, '/comments/user/<int:user_id>')
api.add_resource(comment.CommentByMangaId, '/comments/manga/<int:manga_id>')
api.add_resource(comment.CommentByUserIdMangaId, '/comments/user/<int:user_id>/manga/<int:manga_id>')

@app.route('/mangalist')
def get_mangas():
    url = "https://api.mangadex.org/manga"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    mangas = []
    # print(dict.keys())
    # print(dict["results"])
    for manga in dict["data"]:
        title = manga["attributes"]["title"]["en"]
        descriptionEnglish = manga["attributes"]["description"]["en"]
        # descriptionKorean = manga["attributes"]["description"]["ko"]
        linkToRaw = manga["attributes"]["links"]["raw"]
        publicationDemographic = manga["attributes"]["publicationDemographic"]
        status = manga["attributes"]["status"]
        year = manga["attributes"]["year"]
        tags = [tag["attributes"]["name"]["en"] for tag in manga["attributes"]["tags"]]
        state = manga["attributes"]["state"]
        createdAt = manga["attributes"]["createdAt"]
        updatedAt = manga["attributes"]["updatedAt"]
        relationships = manga["relationships"]
        relationshipId = manga["relationships"][0]["id"]
        relationshipType = manga["relationships"][0]["type"]

        mangas.append({"title": title, "descriptionEnglish":descriptionEnglish, "linkToRaw":linkToRaw, "publicationDemographic": publicationDemographic, "status": status, "year": year, "tags":tags, "state":state, "createdAt":createdAt, "updatedAt":updatedAt, "relationships":relationships, "relationshipId":relationshipId, "relationshipType": relationshipType})
        
        # Print the title
        print(title)

    return {"data": mangas}

if __name__ == '__main__':
    app.run(debug=True)