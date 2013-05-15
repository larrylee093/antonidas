# -*- coding:utf-8 -*-
from datetime import datetime

from models import db, desc
from models.base import BaseComment

class Comment(db.Model, BaseComment):
    __tablename__ = 'comment'
    __table_args__ = (db.Index('type_target_author', 'type', 'target', 'author'), )

    def __init__(self, target, author, text, time, ref_id, type):
        self.target = target
        self.author = author
        self.text = text
        self.time = time
        self.ref_id = ref_id
        self.type = type

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def gets(cls, ids):
        return [cls.get(i) for i in ids]

    @classmethod
    def add(cls, target, author, text, type, ref_id=0):
        c = cls(target, author, text, datetime.now(), ref_id, type)
        db.session.add(c)
        db.session.commit()
        return c

    @classmethod
    def get_ids(cls):
        return db.session.query(cls.id)

def get_comment(id):
    return Comment.get(id)

def get_comments(ids):
    return Comment.gets(ids)

def add_comment(author, target, text, type, ref_id=0):
    return Comment.add(target, author, text, type, ref_id)
    
def get_comment_by_app(type, target, start, limit):
    query = Comment.get_ids().filter_by(type=type, target=target).order_by(desc(Comment.id))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, [r for r, in rs]
