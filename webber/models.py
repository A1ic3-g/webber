from flask_login import UserMixin
from . import db
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

class User(UserMixin, db.Model):
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    #email
    email = db.Column(db.String(100), unique=True)
    #password
    password = db.Column(db.String(100))
    #name
    name = db.Column(db.String(1000))

Declarative_base = declarative_base()

class Mod(Declarative_base):
    __tablename__ = "mod"

    # Primary key
    mod_id = Column(Integer, primary_key=True)
    # mod symlink name
    mod_name = Column(String, unique=True)

