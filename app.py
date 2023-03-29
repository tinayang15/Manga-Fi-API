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
    for manga in dict["data"]:
        try:
            descriptionEnglish = manga["attributes"]["description"]["en"]
        except KeyError:
            descriptionEnglish = "No English Description Available"
        id = manga ["id"]
        title = manga["attributes"]["title"]["en"]
        try:
            linkToRaw = manga["attributes"]["links"]["raw"]
        except KeyError:
            linkToRaw = "No Raw Links Found"
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
        cover_art_id = ""
        for relationship in manga["relationships"]:
            if relationship["type"] == "cover_art":
                cover_art_id = relationship["id"]
        cover_art_url = f"https://api.mangadex.org/cover/{cover_art_id}/"

        author_id = None
        for relationship in manga["relationships"]:
            if relationship["type"] == "author":
                author_id = relationship["id"]
                break

        author_name = None
        if author_id:
            author_url = f"https://api.mangadex.org/author/{author_id}"
            author_response = urllib.request.urlopen(author_url)
            author_data = author_response.read()
            author_dict = json.loads(author_data)
            author_name = author_dict["data"]["attributes"]["name"]
        
        mangas.append({
            "id": id,
            "title": title,
            "descriptionEnglish": descriptionEnglish,
            "linkToRaw": linkToRaw,
            "publicationDemographic": publicationDemographic,
            "status": status,
            "year": year,
            "tags": tags,
            "state": state,
            "createdAt": createdAt,
            "updatedAt": updatedAt,
            "relationships": relationships,
            "relationshipId": relationshipId,
            "relationshipType": relationshipType,
            "cover_art_url": cover_art_url,
            "author_name": author_name
        })

    return {"data": mangas}


# @app.route('/mangalist')
# def get_mangas():
#     url = "https://api.mangadex.org/manga"

#     response = urllib.request.urlopen(url)
#     data = response.read()
#     dict = json.loads(data)

#     mangas = []
#     # print(dict.keys())
#     # print(dict["results"])
#     for manga in dict["data"]:
#         try:
#             descriptionEnglish = manga["attributes"]["description"]["en"]
#         except KeyError:
#             descriptionEnglish = "No English Description Available"
#         id = manga ["id"]
#         title = manga["attributes"]["title"]["en"]
#         # descriptionEnglish = manga["attributes"]["description"]["en"]
#         # descriptionKorean = manga["attributes"]["description"]["ko"]
#         # linkToRaw = manga["attributes"]["links"]["raw"]
#         try:
#             linkToRaw = manga["attributes"]["links"]["raw"]
#         except KeyError:
#             linkToRaw = "No Raw Links Found"
#         publicationDemographic = manga["attributes"]["publicationDemographic"]
#         status = manga["attributes"]["status"]
#         year = manga["attributes"]["year"]
#         tags = [tag["attributes"]["name"]["en"] for tag in manga["attributes"]["tags"]]
#         state = manga["attributes"]["state"]
#         createdAt = manga["attributes"]["createdAt"]
#         updatedAt = manga["attributes"]["updatedAt"]
#         relationships = manga["relationships"]
#         relationshipId = manga["relationships"][0]["id"]
#         relationshipType = manga["relationships"][0]["type"]

#         mangas.append({"id": id, "title": title, "descriptionEnglish":descriptionEnglish, "linkToRaw":linkToRaw, "publicationDemographic": publicationDemographic, "status": status, "year": year, "tags":tags, "state":state, "createdAt":createdAt, "updatedAt":updatedAt, "relationships":relationships, "relationshipId":relationshipId, "relationshipType": relationshipType})
        
#         # Print the title
#         print(title)

#     return {"data": mangas}


# @app.route('/manga/<string:manga_id>')
# def get_manga(manga_id):
#     url = f"https://api.mangadex.org/manga/{manga_id}"

#     response = urllib.request.urlopen(url)
#     data = response.read()
#     dict = json.loads(data)

#     title = dict["data"]["attributes"]["title"]["en"]
#     description = dict["data"]["attributes"]["description"]["en"]
#     linkToRaw = dict["data"]["attributes"]["links"]["raw"]
#     publicationDemographic = dict["data"]["attributes"]["publicationDemographic"]
#     status = dict["data"]["attributes"]["status"]
#     year = dict["data"]["attributes"]["year"]
#     tags = [tag["attributes"]["name"]["en"] for tag in dict["data"]["attributes"]["tags"]]
#     state = dict["data"]["attributes"]["state"]
#     createdAt = dict["data"]["attributes"]["createdAt"]
#     updatedAt = dict["data"]["attributes"]["updatedAt"]
#     relationships = []
#     for relationship in dict["data"]["relationships"]:
#         relationship_id = relationship['id']
#         relationship_type = relationship["type"]
#         relationship_dict={'id': relationship_id, "type": relationship_type}
#         relationships.append(relationship_dict) 
#     author_id = ""
#     for relationship in dict["data"]["relationships"]:
#         if relationship["type"] == "author":
#             author_id = relationship["id"]
#     cover_art_id = ""
#     for relationship in dict["data"]["relationships"]:
#         if relationship["type"] == "cover_art":
#             cover_art_id = relationship["id"]
#     artist_id = ""
#     for relationship in dict["data"]["relationships"]:
#         if relationship["type"] == "artist":
#             artist_id = relationship["id"]
#     relationshipId = dict["data"]["relationships"][0]["id"]
#     relationshipType = dict["data"]["relationships"][0]["type"]

#     manga = {"id": manga_id, "title": title, "description": description, "linkToRaw": linkToRaw, "publicationDemographic": publicationDemographic, "status": status, "year": year, "tags": tags, "state": state, "createdAt": createdAt, "updatedAt": updatedAt, "relationships": relationships, "relationshipId": relationshipId, "relationshipType": relationshipType, "author_id":author_id, "cover_art_id": cover_art_id, "artist_id":artist_id}

#     return {"data": manga}

@app.route('/manga/<string:manga_id>/chapters')
def get_chapter(manga_id):
    url = f"https://api.mangadex.org/manga/{manga_id}/aggregate"

    response = urllib.request.urlopen(url)
    data = response.read()
    manga_data = json.loads(data)

    volumes = manga_data["volumes"]
    manga = []
    for volume in volumes.values():
        volume_number = volume["volume"]
        for chapter in volume["chapters"].values():
            chapter_number = chapter["chapter"]
            chapter_id = chapter["id"]
            manga.append({"volume": volume_number, "chapter": chapter_number, "id": chapter_id})

    return {"data": manga}


@app.route('/manga/chapter/detail/<string:chapter_id>')
def get_chapter_detail(chapter_id):
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}"

    response = urllib.request.urlopen(url)
    data = response.read()
    chapter_data = json.loads(data)

    baseUrl = chapter_data["baseUrl"]
    hash = chapter_data["chapter"]["hash"]
    chapterData = chapter_data["chapter"]["data"]
    dataSaver = chapter_data["chapter"]["dataSaver"]

    chapter={"baseUrl": baseUrl, "hash":hash, "chapterData": chapterData, "dataSaver": dataSaver}


    return {"data": chapter}

# @app.route('/manga/author/<string:author_id>')
# def get_author(author_id):
#     url = f"https://api.mangadex.org/author/{author_id}"

#     response = urllib.request.urlopen(url)
#     data = response.read()
#     author_data = json.loads(data)

#     name = author_data["data"]["attributes"]["name"]

#     author={"name": name}

#     return {"data": author}

# @app.route('/manga/cover/<string:cover_art_id>')
# def get_cover(cover_art_id):
#     url = f"https://api.mangadex.org/cover/{cover_art_id}"

#     response = urllib.request.urlopen(url)
#     data = response.read()
#     cover_art_data = json.loads(data)

#     fileName = cover_art_data["data"]["attributes"]["fileName"]

#     cover_art={"fileName": fileName}

#     return {"data": cover_art}

# @app.route('/manga/<string:manga_id>/cover/<string:fileName>')
# def get_manga_cover(fileName, manga_id):
#     url = f"https://uploads.mangadex.org/covers/{manga_id}/{fileName}"

#     return url

if __name__ == '__main__':
    app.run(debug=True)