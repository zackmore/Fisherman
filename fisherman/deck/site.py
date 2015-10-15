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

from ..basket.basket import Topic, User, Weibo 


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
@view('topics')
def topics():
    return dict(topics=DB.query(Topic).all())


@route('/users')
@view('users')
def users():
    return dict(users=DB.query(User).all())


@route('/weibos')
@view('weibos')
def weibos():
    return dict(weibos=DB.query(Weibo).all())


# Run Server
def run_server():
    run()


if __name__ == '__main__':
    run_server()
