from datetime import datetime
from models.db import db

class User(db.Model):
    __tablename__ = 'users'