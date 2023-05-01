from flask import Flask, render_template, jsonify
import urllib.request, json
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
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
#stops our database from tracking modifications of objects - everytime we make a change to our models, SQLAlchemy caches those changes can lead to high memory usage by our app.
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/manga_fi"
# what database to use
app.config['SQLALCHEMY_ECHO'] = True
# DATABASE_URL = os.getenv('DATABASE_URL')
# if DATABASE_URL:
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace(
#         "://", "ql://", 1)
#     app.config['SQLALCHEMY_ECHO'] = False
#     app.env = 'production'
# else:
#     app.debug = True
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/<Your Database Name>'
#     app.config['SQLALCHEMY_ECHO'] = True

cloudinary.config(
    cloud_name = "dfmp3faei",
    api_key = "354349187816716",
    api_secret = "G9heAJ8GXFQiUCbCLZsDmE8GnNk",
)
db.init_app(app)
migrate = Migrate(app,db)

api.add_resource(user.Users, '/users')
api.add_resource(user.UserDetail, '/users/<int:user_id>')
api.add_resource(user.UserDetailComments, '/users/comments/<int:user_id>')

api.add_resource(user_manga_list.User_Manga_Lists, '/user_manga_lists')
api.add_resource(user_manga_list.User_Manga_List_Detail, '/user_manga_lists/<int:user_manga_list_id>')
api.add_resource(user_manga_list.UserMangaListByUserId, '/user_manga_lists/user/<int:user_id>')
api.add_resource(user_manga_list.UserMangaListByMangaId, '/user_manga_lists/manga/<string:manga_id>')
api.add_resource(user_manga_list.UserMangaListByUserIdMangaId, '/user_manga_lists/user/<int:user_id>/manga/<string:manga_id>')

api.add_resource(comment.Comments, '/comments')
api.add_resource(comment.CommentDetail, '/comments/<int:comment_id>')
api.add_resource(comment.CommentByUserId, '/comments/user/<int:user_id>')
api.add_resource(comment.CommentByMangaId, '/comments/manga/<string:manga_id>')
api.add_resource(comment.CommentByUserIdMangaId, '/comments/user/<int:user_id>/manga/<string:manga_id>')

@app.route('/mangalist')
def get_mangas():
    url = "https://api.mangadex.org/manga"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    mangas = []
    for manga in dict["data"]:
        # try:
        #     description_english = manga["attributes"]["description"]["en"]
        # except KeyError:
        #     description_english = "No English Description Available"
        manga_id = manga ["id"]
        try:
            title = manga["attributes"]["title"]["en"]
        except KeyError:
            title = "No English Title Available"

        # try:
        #     link_to_raw = manga["attributes"]["links"]["raw"]
        # except KeyError:
        #     link_to_raw = "No Raw Links Found"
        # publication_demographic = manga["attributes"]["publicationDemographic"]
        # status = manga["attributes"]["status"]
        # year = manga["attributes"]["year"]
        tags = [tag["attributes"]["name"]["en"] for tag in manga["attributes"]["tags"]]
        # state = manga["attributes"]["state"]
        # created_at = manga["attributes"]["createdAt"]
        # updated_at = manga["attributes"]["updatedAt"]
        relationships = manga["relationships"]
        relationship_id = manga["relationships"][0]["id"]
        relationship_type = manga["relationships"][0]["type"]
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
        
        cover_art_response = urllib.request.urlopen(cover_art_url)
        cover_art_data = cover_art_response.read()
        cover_art_dict = json.loads(cover_art_data)
        file_name = cover_art_dict["data"]["attributes"]["fileName"]
        
        cover_url = get_manga_cover(file_name, manga_id)
        
        mangas.append({
            "manga_id": manga_id,
            "title": title,
            # "description_english": description_english,
            # "link_to_raw": link_to_raw,
            # "publication_demographic": publication_demographic,
            # "status": status,
            # "year": year,
            "tags": tags,
            # "state": state,
            # "created_at": created_at,
            # "updated_at": updated_at,
            "relationships": relationships,
            "relationship_id": relationship_id,
            "relationship_type": relationship_type,
            "cover_url": cover_url,
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


@app.route('/manga/<string:manga_id>')
def get_manga(manga_id):
    url = f"https://api.mangadex.org/manga/{manga_id}"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    manga_id= dict["data"]["id"]
    try:
        title = dict["data"]["attributes"]["title"]["en"]
    except KeyError:
        title = "No English Title Available"
    try:
        description = dict["data"]["attributes"]["description"]["en"]
    except KeyError:
        description = "No English Description Available"
    # linkToRaw = dict["data"]["attributes"]["links"]["raw"]
    publication_demographic = dict["data"]["attributes"]["publicationDemographic"]
    status = dict["data"]["attributes"]["status"]
    try:
        year = dict["data"]["attributes"]["year"]
    except KeyError:
        year = "No year available"
    tags = [tag["attributes"]["name"]["en"] for tag in dict["data"]["attributes"]["tags"]]
    state = dict["data"]["attributes"]["state"]
    try:
        created_at = dict["data"]["attributes"]["createdAt"]
    except KeyError:
        created_at = "No year/date available"
    updated_at = dict["data"]["attributes"]["updatedAt"]
    relationships = []
    for relationship in dict["data"]["relationships"]:
        relationship_id = relationship['id']
        relationship_type = relationship["type"]
        relationship_dict={'id': relationship_id, "type": relationship_type}
        relationships.append(relationship_dict) 
    # author_id = ""
    # for relationship in dict["data"]["relationships"]:
    #     if relationship["type"] == "author":
    #         author_id = relationship["id"]
    # cover_art_id = ""
    # for relationship in dict["data"]["relationships"]:
    #     if relationship["type"] == "cover_art":
    #         cover_art_id = relationship["id"]
    artist_id = ""
    for relationship in dict["data"]["relationships"]:
        if relationship["type"] == "artist":
            artist_id = relationship["id"]
    relationship_id = dict["data"]["relationships"][0]["id"]
    relationship_type = dict["data"]["relationships"][0]["type"]
    cover_art_id = ""
    for relationship in dict["data"]["relationships"]:
        if relationship["type"] == "cover_art":
            cover_art_id = relationship["id"]
    cover_art_url = f"https://api.mangadex.org/cover/{cover_art_id}/"

    author_id = None
    for relationship in dict["data"]["relationships"]:
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
    
    cover_art_response = urllib.request.urlopen(cover_art_url)
    cover_art_data = cover_art_response.read()
    cover_art_dict = json.loads(cover_art_data)
    file_name = cover_art_dict["data"]["attributes"]["fileName"]
    
    cover_url = get_manga_cover(file_name, manga_id)
    chapters = get_chapter(manga_id)

    manga = {"id": manga_id, "title": title, "description": description, "publication_demographic": publication_demographic, "status": status, "year": year, "tags": tags, "state": state, "created_at": created_at, "updated_at": updated_at, "relationships": relationships, "relationship_id": relationship_id, "relationship_type": relationship_type, "author_id":author_id, "author_name": author_name,"cover_art_id":cover_art_id, "cover_url":cover_url, "artist_id":artist_id, "chapters":chapters}

    return {"data": manga}

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

# @app.route('/manga/<string:manga_id>/cover/<string:file_name>')
# def get_manga_cover(file_name, manga_id):
#     url = f"https://uploads.mangadex.org/covers/{manga_id}/{file_name}"

#     return url

@app.route('/manga-cover/<string:manga_id>/cover/<string:file_name>')
def get_manga_cover(file_name, manga_id):
    response = cloudinary.uploader.upload("https://uploads.mangadex.org/covers/{manga_id}/{file_name}".format(file_name))

    return jsonify({
        "url": response["secure_url"]
    })

if __name__ == '__main__':
    app.run()