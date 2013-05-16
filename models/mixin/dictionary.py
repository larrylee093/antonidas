# -*- coding:utf-8 -*-
from datetime import datetime

class DictMixin(object):
    '''
    mixin了这个类的类如果有__dict_keys__这个属性,
    就会把这个list/tuple里的值转成dict, 给json化用.
    如果有一些额外的值需要修改, 需要有__to_dict__这个方法.
    __to_dict__返回一个需要更新的dict
    '''

    def to_dict(self):
        d = {}
        if not hasattr(self, '__dict_keys__'):
            return d
        _dk = self.__dict_keys__
        if not isinstance(_dk, (tuple, list)):
            return d
        for k in _dk:
            value = getattr(self, k, None)
            if value:
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                d[k] = value
        if hasattr(self, '__to_dict__'):
            _d = self.__to_dict__()
            if isinstance(_d, dict):
                d.update(_d)
        return d

