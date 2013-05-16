# -*- coding:utf-8 -*-

CAN_VIEW_ALL = 0
CAN_VIEW_FRIENDS = 1
CAN_VIEW_SELF = 2
CAN_VIEW_NONE = 3

PRIVACY_MAPPING = dict((v, k[9:].lower()) for k, v in locals().items()
    if k.startswith('CAN_VIEW'))

