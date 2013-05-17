# -*- coding:utf-8 -*-
import marshal
from datetime import datetime

from models import db, desc
from models.base import BaseComment
from models.mixin.dictionary import DictMixin
from models.consts import (PRIVACY_MAPPING, CAN_VIEW_ALL, CAN_VIEW_FRIENDS,
        CAN_VIEW_NONE, CAN_VIEW_SELF)

class Comment(db.Model, BaseComment, DictMixin):
    __tablename__ = 'comment'
    _likers = db.Column('likers', db.Binary, nullable=True)
    __table_args__ = (db.Index('type_target_author', 'type', 'target_id', 'author_id'), )
    __dict_keys__ = ('id', 'target_id', 'author_id', 'text', 'time',
            'ref_id', 'likers', 'n_likers')

    def __init__(self, target_id, author_id, text, time, ref_id, type, privacy, likers):
        self.target_id = target_id
        self.author_id = author_id
        self.text = text
        self.time = time
        self.ref_id = ref_id
        self.type = type
        self.privacy = privacy
        self._likers = likers

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def gets(cls, ids):
        return [cls.get(i) for i in ids]

    @classmethod
    def add(cls, target_id, author_id, text, type, ref_id, privacy, likers):
        likers = marshal.dumps(likers)
        c = cls(target_id, author_id, text, datetime.now(), ref_id, type, privacy, likers)
        db.session.add(c)
        db.session.commit()
        return c

    @classmethod
    def get_ids(cls):
        return db.session.query(cls.id)

    def delete(self, user_id):
        if user_id != self.author_id:
            return
        db.session.delete(self)
        db.session.commit()

    def can_view(self, visitor_id):
        #TODO 补上get_user
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

    def ref_comment(self):
        return get_comment(self.ref_id) if self.ref_id else None

    def author(self):
        #TODO 补上get_user
        pass

    def like(self, user_id):
        if user_id in self.likers or user_id == self.author_id:
            return
        likers = self.likers.append(user_id)
        self._likers = marshal.dumps(likers)
        db.session.query(self.__class__).filter_by(id=self.id).update(dict(likers=self._likers))
        db.session.commit()

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
    return Comment.add(target_id, author_id, text, type, ref_id, privacy, likers)
    
def get_comment_by_type(type, target_id, start, limit):
    '''某入口下的评论'''
    query = Comment.get_ids().filter_by(type=type, target_id=target_id).order_by(desc(Comment.id))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, [r for r, in rs]

def get_comment_by_user(type, target_id, user_id, start, limit):
    '''只看楼主(其实随便哪个都可以啦)'''
    query = Comment.get_ids().filter_by(type=type, target_id=target_id, author_id=author_id).order_by(desc(Comment.id))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, [r for r, in rs]
