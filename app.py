from flask import Flask
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
api.add_resource(user_manga_list.User_Manga_List, '/user_manga_lists')
api.add_resource(user_manga_list.User_Manga_List_Detail, '/user_manga_lists/<int:user_manga_list_id>')
api.add_resource(user_manga_list.User_Manga_List_Detail, '/user_manga_lists/user/<int:user_id>')
api.add_resource(user_manga_list.User_Manga_List_Detail, '/user_manga_lists/manga/<int:manga_id>')
api.add_resource(user_manga_list.User_Manga_List_Detail, '/user_manga_lists/user/<int:user_id>/manga/<int:manga_id>')
api.add_resource(comment.Comments, '/comments')
api.add_resource(comment.CommentDetail, '/comments/<int:comment_id>')

if __name__ == '__main__':
    app.run()