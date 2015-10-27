# -*- coding: utf-8 -*-

import pdb

import re
import sys
import json
import time
import urllib
import os.path
import requests

from bottle import route, view, run, template, static_file, request
from bottle import TEMPLATE_PATH
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..basket.basket import Topic,\
                            TopicUser,\
                            TopicWeibo,\
                            RepostWeibo,\
                            RepostUser


# Global Variables, Bottle Settings, Helpers
################################################
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


class Helper(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_listpage_resource(resource, current_page):
        item_per_page = int(config['deck']['item_per_page'])
        if current_page == 0 or current_page == 1:
            start = 0
            end = item_per_page
        else:
            start = item_per_page * current_page
            end = start + item_per_page
        q = DB.query(resource).slice(start, end)

        return q

    @staticmethod
    def generate_pagination(all_count, current_page, query_url):
        rtn = {}

        item_per_page = int(config['deck']['item_per_page'])
        rtn['pages'] = all_count / item_per_page + 1
        rtn['prev'] = query_url + '/' + str(current_page - 1)
        rtn['next'] = query_url + '/' + str(current_page + 1)
        rtn['has_prev'] = True
        rtn['has_next'] = True
        if current_page == 0 or current_page == 1:
            rtn['has_prev'] = False
        if current_page == rtn['pages'] - 1:
            rtn['has_next'] = False

        return rtn


# Static Resources
################################################
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__),
                        'static/'))


# Pages
################################################
@route('/')
@route('/dashboard')
@view('dashboard')
def dashboard():
    pass


@route('/topics')
@route('/topics/<page:int>')
@view('topics/topics')
def topics(page=0):
    resource = Helper.generate_listpage_resource(Topic, page)
    pagination = Helper.generate_pagination(DB.query(Topic).count(),
                                            page,
                                            '/topics')
    return dict(topics=resource, pagination=pagination)


@route('/topics/users')
@route('/topics/users/<page:int>')
@view('topics/users')
def topicUsers(page=0):
    resource = Helper.generate_listpage_resource(TopicUser, page)
    pagination = Helper.generate_pagination(DB.query(TopicUser).count(),
                                                    page,
                                                    '/topics/users')
    return dict(users=resource, pagination=pagination)


@route('/topics/weibos')
@route('/topics/weibos/<page:int>')
@view('topics/weibos')
def topicWeibos(page=0):
    resource = Helper.generate_listpage_resource(TopicWeibo, page)
    pagination = Helper.generate_pagination(DB.query(TopicWeibo).count(),
                                                    page,
                                                    '/topics/weibos')
    return dict(weibos=resource, pagination=pagination)


@route('/reposts')
@route('/reposts/<page:int>')
@view('reposts/reposts')
def reposts(page=0):
    resource = Helper.generate_listpage_resource(RepostWeibo, page)
    pagination = Helper.generate_pagination(DB.query(RepostWeibo).count(),
                                                    page,
                                                    '/reposts')
    return dict(reposts=resource, pagination=pagination)


@route('/reposts/users')
@route('/reposts/users/<page:int>')
@view('reposts/users')
def repostUsers(page=0):
    resource = Helper.generate_listpage_resource(RepostUser, page)
    pagination = Helper.generate_pagination(DB.query(RepostUser).count(),
                                                    page,
                                                    '/reposts/users')
    return dict(users=resource, pagination=pagination)


# Run Server
################################################
def run_server():
    run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    run_server()
