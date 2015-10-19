# -*- coding: utf-8 -*-

import pdb

import re
import sys
import json
import time
import urllib
import os.path
import requests

from bottle import route, view, run, template, static_file
from bottle import TEMPLATE_PATH
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..basket.basket import Topic,\
                            TopicUser,\
                            TopicWeibo,\
                            RepostWeibo,\
                            RepostUser


# Global Variables and Bottle Settings
config_path = os.path.join(os.path.dirname(__file__),
                            '../../config.json')
with open(config_path) as config_file:
    config = json.load(config_file)
    db_path = config['basket']['path']
    engine = create_engine(db_path)
    Session = sessionmaker(bind=engine)
    DB = Session()

TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                        'views')))


# Static Resources
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__),
                        'static/'))


# Pages
@route('/')
@route('/dashboard')
@view('dashboard')
def dashboard():
    pass


@route('/topics')
@view('topics/topics')
def topics():
    return dict(topics=DB.query(Topic).all())


@route('/topics/users')
@view('topics/users')
def topicUsers():
    return dict(users=DB.query(TopicUser).all())


@route('/topics/weibos')
@view('topics/weibos')
def topicWeibos():
    return dict(weibos=DB.query(TopicWeibo).all())


@route('/reposts')
@view('reposts/reposts')
def reposts():
    return dict(reposts=DB.query(RepostWeibo).all())


@route('/reposts/users')
@view('reposts/users')
def repostUsers():
    return dict(users=DB.query(RepostUser).all())


# Run Server
def run_server():
    run()


if __name__ == '__main__':
    run_server()
