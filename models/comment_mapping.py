# -*- coding:utf-8 -*-
from models import db
from models.base import BaseMapping

class CommentMapping(db.Model, BaseMapping):
    __tablename__ = 'comment_mapping'

    def __init__(self, app):
        self.app = app

    @classmethod
    def register(cls, app):
        mapping = cls(app)
        db.session.add(mapping)
        db.session.commit()
        return mapping.id

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def gets(cls, ids):
        return [cls.get(id) for id in ids]

    @classmethod
    def get_id_by_name(cls, app):
        m = db.session.query(cls.id).filter_by(app=app).first()
        return m and m.id or None

    @classmethod
    def get_name_by_id(cls, id):
        m = cls.get(id)
        return m and m.app or None

def get_mapping(id):
    return CommentMapping.get(id)

def get_name_by_id(id):
    return CommentMapping.get_name_by_id(id)

def get_id_by_name(id):
    return CommentMapping.get_id_by_name(id)

def register_app(app):
    return CommentMapping.register(app)
