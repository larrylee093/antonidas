# -*- coding:utf-8 -*-
from datetime import datetime
from models import db

class BaseComment(object):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    target_id = db.Column('target_id', db.Integer, nullable=False)
    author_id = db.Column('author_id', db.Integer, nullable=False, index=True)
    text = db.Column('text', db.Text, nullable=False)
    time = db.Column('time', db.DateTime, default=datetime.now)
    ref_id = db.Column('ref_id', db.Integer, default=0)
    type = db.Column('type', db.Integer, nullable=False)
    privacy = db.Column('privacy', db.Integer, nullable=False)

class BaseMapping(object):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    app = db.Column('app', db.String(37), index=True)

class DictMixin(object):

    def to_dict(self):
        d = {}
        if not hasattr(self, '__dict_keys__'):
            return d
        _dk = self.__dict_keys__
        if not isinstance(_dk, (tuple, list)):
            return d
        for k in _dk:
            value = getattr(self, k, None)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            if value:
                d[k] = value
        if hasattr(self, '__to_dict__'):
            _d = self.__to_dict__()
            if isinstance(_d, dict):
                d.update(_d)
        return d

