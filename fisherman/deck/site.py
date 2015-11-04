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
import threading

from rq import Queue
from redis import Redis

from bottle import view, run, template, static_file, request, redirect
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

from helper import Helper, worker_pelican


# Global Variables, Bottle Settings
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
redis_conn = Redis()
Q = Queue(connection=redis_conn)


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
def topics_users(page=0):
    topic_id = request.query.get('topic_id')
    if topic_id:
        topic_id = int(topic_id)

    rtn = Helper.generate_listpage_resource(TopicUser,
                                            page,
                                            'name',
                                            '/topics/users',
                                            topic_id=topic_id)
    return dict(users=rtn['resource'], pagination=rtn['pagination'])


@route('/topics/weibos')
@route('/topics/weibos/<page:int>')
@view('topics/weibos')
def topics_weibos(page=0):
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
def reposts_users(page=0):
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
def bigvs_followers(page=0):
    rtn = Helper.generate_listpage_resource(BigVFollower,
                                            page,
                                            'name',
                                            '/bigvs/followers')
    return dict(followers=rtn['resource'], pagination=rtn['pagination'])


@get('/settings/token')
@view('settings/token')
def settings_token_show():
    config_path = os.path.join(os.path.dirname(__file__),
                                '../../config.json')
    with open(config_path) as config_file:
        config = json.load(config_file)
        token = config['pelican']['token'][0]

        token_str = []
        for pair in token.items():
            token_str.append(pair[0] + ':' + pair[1] + '\n')

        config_file.close()
        return dict(request_header=''.join(token_str))


@post('/settings/token')
def settings_token_update():
    new_token = request.forms.get('request-header').split('\r\n')
    new_token_list = [s for s in new_token if s.strip()]
    new_token_dict = {}
    for pair in new_token_list:
        kv = pair.split(':')
        new_token_dict[kv[0]] = kv[1]
    config['pelican']['token'][0] = new_token_dict

    with open(config_path, 'w') as config_file:
        config_file.write(json.dumps(config))
        config_file.close()

    redirect('/')


# Job Queue
################################################
@post('/fetch/topic/<topic_id:int>')
def fetch_topic(topic_id):
    topic = DB.query(Topic).filter_by(id=topic_id).first()
    Q.enqueue(worker_pelican, 'topic', topic.name)
    return {'result': 1}

# Run Server
################################################
def run_server():
    run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    run_server()
