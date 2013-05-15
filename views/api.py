# -*- coding:utf-8 -*-

from flask import Blueprint, abort, request, jsonify
from models.comment_mapping import register_app
from models.dispatcher import GateKeeper
from models.comment import get_comment

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
    r = GateKeeper.add_comment(app, int(author), int(target), text)
    return jsonify(r)

@api.route('/comment/<int:cid>/')
def comment(cid):
    c = get_comment(cid)
    r = {
        'id': c.id,
        'text': c.text,
        'author': c.author,
        'ref_id': c.ref_id,
        'type': c.type
        }
    return jsonify(r)

@api.route('/register/<app>/')
def register(app):
    r = register_app(app)
    return str(r)

