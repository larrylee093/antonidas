# -*- coding:utf-8 -*-

from flask import Blueprint, abort, request, jsonify

from sheep.api.users import generate_login_url

from models.mapping import register_app
from models.comment import get_comment
from models.dispatcher import DalaranKeeper

api = Blueprint('api', __name__)

TEST_PAGE = """\
<!DOCTYPE HTML>
<html lang="en">
  <head>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.4.1.min.js">
    </script>
    <meta charset="UTF-8">
    <title></title>
  </head>
  <body>
    <a href="%s">点我登录</a>
  </body>
</html>
""" % generate_login_url()

@api.route('/')
def index():
    return TEST_PAGE

@api.route('/add_comment/')
def add_comment():
    author = request.args.get('a')
    target = request.args.get('t')
    app = request.args.get('app')
    text = request.args.get('e')
    r = DalaranKeeper.add_comment(app, int(author), int(target), text, likers=[1,2,3])
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

