#!/usr/bin/python
# encoding: UTF-8

import logging
import config

from flask import Flask, redirect, url_for
from sheep.api.sessions import SessionMiddleware, FilesystemSessionStore

from models import init_db
from views.api import api

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = config.DEBUG

app.config.update(
        SQLALCHEMY_DATABASE_URI = config.DATABASE_URI,
        SQLALCHEMY_POOL_SIZE = 100,
        SQLALCHEMY_POOL_TIMEOUT = 10,
        SQLALCHEMY_POOL_RECYCLE = 3600,
        SESSION_COOKIE_DOMAIN = config.SESSION_COOKIE_DOMAIN,
)

app.register_blueprint(api, url_prefix='/api')

init_db(app)

app.wsgi_app = SessionMiddleware(app.wsgi_app,
        FilesystemSessionStore(),
        cookie_name=config.SESSION_KEY,
        cookie_path='/',
        cookie_domain=config.SESSION_COOKIE_DOMAIN)

@app.route('/')
def index():
    return redirect(url_for('api.index'))

