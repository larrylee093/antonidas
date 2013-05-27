# -*- coding:utf-8 -*-
from sheep.api.cache import cache, backend
from models import db, IntegrityError
from models.base import BaseMapping
from models.mixin.dictionary import DictMixin

_ANTONIDAS_MAPPING_KEY = 'anto:map:%s'

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
        m = DeletedMapping(self.id, self.app)
        db.session.delete(self)
        db.session.add(m)
        db.session.commit()
        _flush_mapping(self.app)

    @classmethod
    def gets(cls, apps):
        return [cls.get(app) for app in apps]

    @classmethod
    @cache(_ANTONIDAS_MAPPING_KEY % '{app}')
    def get(cls, app):
        m = cls.query.filter_by(app=app).first()
        return m or None

    @classmethod
    def get_by_id(cls, id):
        m = cls.query.get(id)
        return m or None

class DeletedMapping(db.Model, BaseMapping):
    __tablename__ = 'deleted_mapping'
    __table_args__ = (db.UniqueConstraint('app', name='uk_app'),)
    __dict_keys__ = ('id', 'app')

    def __init__(self, id, app):
        self.id = id
        self.app = app

    @classmethod
    def get(cls, app):
        m = cls.query.filter_by(app=app).first()
        return m or None

def get_mapping(app):
    return Mapping.get(app)

def register_app(app):
    _m = DeletedMapping.get(app)
    if not _m:
        return Mapping.register(app)
    else:
        return recover_app(app)


def unregister_app(app):
    m = get_mapping(app)
    if not app:
        return
    m.delete()
    _flush_mapping(app)

def recover_app(app):
    m = DeletedMapping.get(app)
    _m = Mapping(m.app)
    _m.id = m.id
    db.session.add(_m)
    db.session.delete(m)
    db.session.commit()
    return _m

def has_registered(app):
    return not (get_mapping(app) is None)

def _flush_mapping(app):
    backend.delete(_ANTONIDAS_MAPPING_KEY % app)
