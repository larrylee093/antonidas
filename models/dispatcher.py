# -*- coding:utf-8 -*-
from models.mapping import get_mapping 
from models.comment import get_comments, add_comment, get_comment_by_type
from models.consts import CAN_VIEW_ALL

class Dispatcher(object):

    def __init__(self, name):
        self.name = name
        self._mapping = {}

    def _add_mapping(self, id, app):
        self._mapping[app] = id

    def _get_mapping(self, app):
        try:
            m = self._mapping[app]
        except KeyError:
            m = get_mapping(app)
            if m:
                self._add_mapping(m.id, app)
            else:
                raise DispatchException('no mapping found')
        return m.id

    def add_comment(self, app, target, author, text, ref_id=0, privacy=CAN_VIEW_ALL, likers=[]):
        m = self._get_mapping(app)
        c = add_comment(target, author, text, m, ref_id, privacy, likers)
        r = {'r': 'ok'}
        return r

    def get_comments(self, app, target, start, limit):
        m = self._get_mappint(app)
        return get_comment_by_type(m, target, start, limit)


class DispatchException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

DalaranKeeper = Dispatcher('antonidas')
