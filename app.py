from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)
api = Api (app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/manga_fi"
app.config['SQLALCHEMY_ECHO'] = True




if __name__ == '__main__':
    app.run()