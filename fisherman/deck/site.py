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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..basket.basket import Topic, User, Weibo 


# Global Variables
config_path = os.path.join(os.path.dirname(__file__),
                            '../../config.json')
with open(config_path) as config_file:
    config = json.load(config_file)
    db_path = config['basket']['path']
    engine = create_engine(db_path)
    Session = sessionmaker(bind=engine)

    DB = Session()


# Static Resources
@route('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root='./static/')


# Pages
@route('/')
@route('/dashboard')
@view('dashboard')
def dashboard():
    pass


@route('/topics')
@view('topics')
def topics():
    return dict(title='Topics')


@route('/users')
@view('users')
def users():
    pass


def main():
    run(host='localhost', port=8080, reloader=True)


# Run Server
if __name__ == '__main__':
    run(host='localhost', port=8080, reloader=True)
