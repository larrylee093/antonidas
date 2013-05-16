# -*- coding:utf-8 -*-

from flask import Blueprint, abort, request, jsonify
from models.mapping import register_app
from models.comment import get_comment
from models.dispatcher import DalaranKeeper

api = Blueprint('api', __name__)

@api.route('/')
def index():
    d = dict([(k, k) for k in globals().keys()])
    return jsonify(d)

@api.route('/add_comment/')
def add_comment():
    author = request.args.get('a')
    target = request.args.get('t')
    app = request.args.get('app')
    text = request.args.get('e')
    r = DalaranKeeper.add_comment(app, int(author), int(target), text, likers=[111111111,222222222222,33333333333])
    return jsonify(r)

@api.route('/comment/<int:cid>/')
def comment(cid):
    c = get_comment(cid)
    return jsonify(c.to_dict())

@api.route('/register/<app>/')
def register(app):
    r = register_app(app)
    if not r:
        r = {'error': 'exists'}
    return str(r)

