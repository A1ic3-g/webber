from webber import db, create_app, models
db.create_all(app=create_app())
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base





engine = create_engine("sqlite:///webber/db.sqlite")
models.Declarative_base.metadata.create_all(engine)