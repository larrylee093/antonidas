# -*- coding:utf-8 -*-
from models import db, IntegrityError
from models.base import BaseMapping
from models.mixin.dictionary import DictMixin

class Mapping(db.Model, BaseMapping, DictMixin):
    __tablename__ = 'mapping'
    __table_args__ = (db.UniqueConstraint('app', name='uk_app'),)
    __dict_keys__ = ('id', 'app')

    def __init__(self, app):
        self.app = app

    @classmethod
    def register(cls, app):
        mapping = cls(app)
        try:
            db.session.add(mapping)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return mapping.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def gets(cls, apps):
        return [cls.get(app) for app in apps]

    @classmethod
    def get(cls, app):
        m = cls.query.filter_by(app=app).first()
        return m or None

    @classmethod
    def get_by_id(cls, id):
        m = cls.query.get(id)
        return m or None

def get_mapping(app):
    return Mapping.get(app)

def register_app(app):
    return Mapping.register(app)

def unregister_app(app):
    m = get_mapping(app)
    if not app:
        return
    m.delete()

def has_registered(app):
    return not (get_mapping(app) is None)
