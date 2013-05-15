# -*- coding:utf-8 -*-
from datetime import datetime
from models import db

class BaseComment(object):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    target = db.Column('target', db.Integer, nullable=False)
    author = db.Column('author', db.Integer, nullable=False, index=True)
    text = db.Column('text', db.Text, nullable=False)
    time = db.Column('time', db.DateTime, default=datetime.now)
    ref_id = db.Column('ref_id', db.Integer, default=0)
    type = db.Column('type', db.Integer, nullable=False)

class BaseMapping(object):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    app = db.Column('app', db.String(32), index=True)

