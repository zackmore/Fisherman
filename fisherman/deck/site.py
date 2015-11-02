# -*- coding: utf-8 -*-

import pdb

import re
import sys
import json
import time
import urllib
import os.path
import requests
import subprocess

from bottle import view, run, template, static_file, request
from bottle import TEMPLATE_PATH
from bottle import route, post, get
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..basket.basket import Topic,\
                            TopicUser,\
                            TopicWeibo,\
                            RepostWeibo,\
                            RepostUser,\
                            BigV,\
                            BigVFollower

from ..pelican.follower import FollowerEater
from ..pelican.repost import RepostEater
from ..pelican.topic import TopicEater


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
    def _get_resource_query(resource, search_column):
        search_keyword = request.query.get('keyword')
        if search_keyword:
            search_keyword = request.query.get('keyword').strip().decode('utf-8')
            q = DB.query(resource).\
                filter(getattr(resource, search_column).\
                        contains(search_keyword))
        else:
            q = DB.query(resource)
        return q

    @staticmethod
    def _paginating_query(q, current_page):
        item_per_page = int(config['deck']['item_per_page'])
        if current_page == 0 or current_page == 1:
            start = 0
            end = item_per_page
        else:
            start = item_per_page * current_page
            end = start + item_per_page
        return q.slice(start, end)

    @staticmethod
    def _get_pagination(all_count, current_page, query_url):
        pagination = {}

        item_per_page = int(config['deck']['item_per_page'])
        pagination['pages'] = all_count / item_per_page + 1
        pagination['prev'] = query_url + '/' + str(current_page - 1)
        pagination['next'] = query_url + '/' + str(current_page + 1)
        pagination['has_prev'] = True
        pagination['has_next'] = True
        if current_page == 0 or current_page == 1:
            pagination['has_prev'] = False
        if current_page == pagination['pages'] - 1:
            pagination['has_next'] = False
        return pagination

    @staticmethod
    def generate_listpage_resource(resource,
                                    current_page,
                                    search_column,
                                    query_url):
        q = Helper._get_resource_query(resource, search_column)
        all_count = q.count()

        resource = Helper._paginating_query(q, current_page)
        pagination = Helper._get_pagination(all_count, current_page, query_url)

        return dict(resource=resource, pagination=pagination)


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
    rtn = Helper.generate_listpage_resource(Topic,
                                            page,
                                            'name',
                                            '/topics')
    return dict(topics=rtn['resource'], pagination=rtn['pagination'])


@route('/topics/users')
@route('/topics/users/<page:int>')
@view('topics/users')
def topicUsers(page=0):
    rtn = Helper.generate_listpage_resource(TopicUser,
                                            page,
                                            'name',
                                            '/topics/users')
    return dict(users=rtn['resource'], pagination=rtn['pagination'])


@route('/topics/weibos')
@route('/topics/weibos/<page:int>')
@view('topics/weibos')
def topicWeibos(page=0):
    rtn = Helper.generate_listpage_resource(TopicWeibo,
                                            page,
                                            'content',
                                            '/topics/weibos')
    return dict(weibos=rtn['resource'], pagination=rtn['pagination'])


@route('/reposts')
@route('/reposts/<page:int>')
@view('reposts/reposts')
def reposts(page=0):
    rtn = Helper.generate_listpage_resource(RepostWeibo,
                                            page,
                                            'content',
                                            '/reposts')
    return dict(reposts=rtn['resource'], pagination=rtn['pagination'])


@route('/reposts/users')
@route('/reposts/users/<page:int>')
@view('reposts/users')
def repostUsers(page=0):
    rtn = Helper.generate_listpage_resource(RepostUser,
                                            page,
                                            'name',
                                            '/reposts/users')
    return dict(users=rtn['resource'], pagination=rtn['pagination'])


@route('/bigvs')
@route('/bigvs/<page:int>')
@view('bigvs/bigvs')
def bigvs(page=0):
    rtn = Helper.generate_listpage_resource(BigV,
                                            page,
                                            'name',
                                            '/bigvs')
    return dict(bigvs=rtn['resource'], pagination=rtn['pagination'])


@route('/bigvs/followers')
@route('/bigvs/followers/<page:int>')
@view('bigvs/followers')
def bigvs(page=0):
    rtn = Helper.generate_listpage_resource(BigVFollower,
                                            page,
                                            'name',
                                            '/bigvs/followers')
    return dict(followers=rtn['resource'], pagination=rtn['pagination'])


# Subprocess
################################################
@get('/fetch/topic/<topic_id:int>')
def fetch_topic(topic_id):
    #return {'topic': topic}
    topic = DB.query(Topic).filter_by(id=topic_id).first()

    pelican = TopicEater()
    pelican.catch(topic.name)


# Run Server
################################################
def run_server():
    run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    run_server()
