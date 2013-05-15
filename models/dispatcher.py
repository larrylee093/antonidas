# -*- coding:utf-8 -*-
from models.comment_mapping import get_name_by_id, get_id_by_name
from models.comment import get_comment, get_comments, add_comment, get_comment_by_app

class Dispatcher(object):

    def __init__(self, name):
        self.name = name
        self._mapping = {}

    def _add_mapping(self, id, app):
        self._mapping[app] = id

    def _get_mapping(self, app):
        if self._mapping.has_key(app):
            m = self._mapping[app]
        else:
            m = get_id_by_name(app)
            if m:
                self._add_mapping(m, app)
            else:
                raise DispatchException('no mapping found')
        return m

    def add_comment(self, app, author, target, text, ref_id=0):
        m = self._get_mapping(app)
        add_comment(author, target, text, m, ref_id)
        r = {'r': 'ok'}

    def get_comments(self, app, target, start, limit):
        m = self._get_mappint(app)
        return get_comment_by_app(m, target, start, limit)


class DispatchException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

GateKeeper = Dispatcher('antonidas')
