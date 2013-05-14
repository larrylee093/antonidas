# -*- coding:utf-8 -*-

from flask import Blueprint, abort

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return 'api'

