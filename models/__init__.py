#-*- coding:utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy, sqlalchemy

IntegrityError = sqlalchemy.exc.IntegrityError
desc = sqlalchemy.desc

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()

