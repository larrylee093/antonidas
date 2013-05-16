# -*- coding:utf-8 -*-
from datetime import datetime

from models import db, desc
from models.base import BaseComment
from models.consts import CAN_VIEW_ALL, CAN_VIEW_FRIENDS, CAN_VIEW_NONE, CAN_VIEW_SELF

class Comment(db.Model, BaseComment):
    __tablename__ = 'comment'
    __table_args__ = (db.Index('type_target_id_author_id', 'type', 'target_id', 'author_id'), )

    def __init__(self, target_id, author_id, text, time, ref_id, type, privacy, likers):
        self.target_id = target_id
        self.author_id = author_id
        self.text = text
        self.time = time
        self.ref_id = ref_id
        self.type = type
        self.privacy = privacy
        self.likers = likers

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def gets(cls, ids):
        return [cls.get(i) for i in ids]

    @classmethod
    def add(cls, target_id, author_id, text, type, ref_id=0, privacy=CAN_VIEW_ALL, likers=[]):
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

    def author(self):
        #TODO 补上get_user
        pass

    def like(self):
        pass

    def to_dict(self):
        pass

def get_comment(id):
    return Comment.get(id)

def get_comments(ids):
    return Comment.gets(ids)

def add_comment(author_id, target_id, text, type, ref_id=0):
    return Comment.add(target_id, author_id, text, type, ref_id)
    
def get_comment_by_app(type, target_id, start, limit):
    query = Comment.get_ids().filter_by(type=type, target_id=target_id).order_by(desc(Comment.id))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, [r for r, in rs]
