# -*- coding:utf-8 -*-
from inspector import getargspec
from functools import wraps

def check_user(f):
    an, av, kw, d = getargspec()
    @wraps(f)
    def _(*a, **kw):
        _a = dict(zip(an, a))
        user_id = _a.pop('user_id', None)
        if not user_id:
            raise Exception('function must contains user_id')
        return f(*a, **kw)
    return _

