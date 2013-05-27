# -*- coding:utf-8 -*-
import marshal
from datetime import datetime

from sheep.api.users import get_user
from sheep.api.cache import cache, npcache, backend

from models import db, desc
from models.base import BaseComment
from models.mixin.dictionary import DictMixin
from models.consts import (PRIVACY_MAPPING, CAN_VIEW_ALL, CAN_VIEW_FRIENDS,
        CAN_VIEW_NONE, CAN_VIEW_SELF)

_ANTONIDAS_COMMENT_KEY = 'anto:c:%s'
_ANTONIDAS_USER_C_KEY = 'anto:ucs:%s:%s:%s'
_ANTONIDAS_APP_C_KEY = 'anto:acs:%s:%s'

class Comment(db.Model, BaseComment, DictMixin):
    __tablename__ = 'comment'
    _likers = db.Column('likers', db.Binary, nullable=True)
    __table_args__ = (db.Index('type_target_author', 'type', 'target_id', 'author_id'), )
    __dict_keys__ = ('id', 'target_id', 'author_id', 'text', 'time',
            'ref_id', 'likers', 'n_likers')

    def __init__(self, target_id, author_id, text, time, type,
            ref_id=0, privacy=CAN_VIEW_ALL, likers=[]):
        self.target_id = target_id
        self.author_id = author_id
        self.text = text
        self.time = time
        self.ref_id = ref_id
        self.type = type
        self.privacy = privacy
        self._likers = likers

    @classmethod
    @cache(_ANTONIDAS_COMMENT_KEY % '{id}')
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def gets(cls, ids):
        return [cls.get(i) for i in ids]

    @classmethod
    def add(cls, target_id, author_id, text, type, ref_id, privacy, likers):
        likers = marshal.dumps(likers)
        c = cls(target_id, author_id, text, datetime.now(), type,
                ref_id=ref_id, privacy=privacy, likers=likers)
        db.session.add(c)
        db.session.commit()
        _flush_user_comment(type, author_id, target_id)
        _flush_app_comment(type, target_id)
        return c

    @classmethod
    def get_ids(cls):
        return db.session.query(cls.id)

    def delete(self, user_id):
        if user_id != self.author_id:
            return
        db.session.delete(self)
        db.session.commit()
        _flush_comment(self.id)
        _flush_user_comment(self.type, self.author_id, self.target_id)
        _flush_app_comment(self.type, self.target_id)

    def can_view(self, visitor_id):
        # TODO 现在存在relationship咩
        return True

    @property
    def is_public(self):
        return self.privacy == CAN_VIEW_ALL

    @property
    def is_private(self):
        return self.privacy == CAN_VIEW_SELF

    @property
    def is_friend_only(self):
        return self.privacy == CAN_VIEW_FRIENDS

    @property
    def is_banned(self):
        return self.privacy == CAN_VIEW_NONE

    def set_privacy(self, privacy):
        if self.privacy == privacy:
            return
        self.privacy = privacy
        db.session.query(self.__class__).filter_by(id=self.id).update(dict(privacy=privacy))
        db.session.commit()
        _flush_comment(self.id)

    def ref_comment(self):
        return get_comment(self.ref_id) if self.ref_id else None

    def author(self):
        return get_user(self.author_id)

    def like(self, user_id):
        if user_id in self.likers or user_id == self.author_id:
            return
        likers = self.likers.append(user_id)
        self._likers = marshal.dumps(likers)
        db.session.query(self.__class__).filter_by(id=self.id).update(dict(likers=self._likers))
        db.session.commit()
        _flush_comment(self.id)

    def __to_dict__(self):
        return {'privacy': PRIVACY_MAPPING.get(self.privacy, '')}

    @property
    def likers(self):
        return marshal.loads(self._likers) if self._likers else []

    @property
    def n_likers(self):
        return len(self.likers)

def get_comment(id):
    return Comment.get(id)

def get_comments(ids):
    return Comment.gets(ids)

def add_comment(target_id, author_id, text, type, ref_id, privacy, likers):
    return Comment.add(target_id, author_id, text, type,
            ref_id=ref_id, privacy=privacy, likers=likers)

@npcache(_ANTONIDAS_APP_C_KEY % ('{type}', '{target_id}'))
def get_comment_by_type(type, target_id, start, limit):
    '''某入口下的评论'''
    query = Comment.get_ids().filter_by(type=type, target_id=target_id).order_by(desc(Comment.id))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, [r for r, in rs]

@npcache(_ANTONIDAS_USER_C_KEY % ('{type}', '{user_id}', '{target_id}'))
def get_comment_by_user(type, target_id, user_id, start, limit):
    '''只看楼主(其实随便哪个都可以啦)'''
    query = Comment.get_ids().filter_by(type=type, target_id=target_id, author_id=author_id).order_by(desc(Comment.id))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, [r for r, in rs]

def _flush_comment(id):
    backend.delete(_ANTONIDAS_COMMENT_KEY % id)

def _flush_user_comment(type, user_id, target_id):
    backend.delete(_ANTONIDAS_USER_C_KEY % (type, user_id, target_id))

def _flush_app_comment(type, target_id):
    backend.delete(_ANTONIDAS_APP_C_KEY % (type, target_id))
