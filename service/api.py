# -*- coding:utf-8 -*-
import app

from models.dispatcher import DalaranKeeper
from models.comment import get_comment as get_comment_c, get_comments as get_comments_c
from models.consts import CAN_VIEW_ALL

def add_comment(app, target, author, text,
        ref_id=0, privacy=CAN_VIEW_ALL, likers=[]):
    c = DalaranKeeper.add_comment(app, target, author, text, ref_id=ref_id,
            privacy=privacy, likers=likers)
    return c.to_dict() if c else dict()

def del_comment(author, cid):
    cmt = get_comment_c(cid)
    if not cmt or cmt.author().uid != author:
        return dict()
    cmt.delete(author)
    return dict(r=0, msg='succ')

def get_comments(app, target, start, limit):
    n, rs = DalaranKeeper.get_comments(app, target, start, limit)
    more = len(rs) == limit
    comments = get_comments_c(rs)
    comments = [c.to_dict() for c in comments if c]
    return dict(total=n, app=app, target=target, more=more, comments=comments)

def register(app):
    r = DalaranKeeper.register(app)
    if r:
        return dict(r=0, msg='succ', res=r)
    else:
        return dict(r=1, msg='has registered')

def unregister(app):
    DalaranKeeper.unregister(app)
    return dict(r=0, msg='succ')

def has_registered(app):
    if DalaranKeeper.has_registered(app):
        return dict(r=0, msg='Y')
    else:
        return dict(r=0, msg='N')

def get_comment(id):
    c = get_comment_c(id)
    return c.to_dict() if c else dict()

