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

from rq     import Queue
from redis  import Redis

from bottle import  view,\
                    run,\
                    template,\
                    static_file,\
                    request,\
                    redirect
from bottle         import TEMPLATE_PATH
from bottle         import route, post, get
from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker

from ..basket.basket import Topic,\
                            TopicUser,\
                            TopicWeibo,\
                            RepostWeibo,\
                            RepostUser,\
                            BigV,\
                            BigVFollower

from ..pelican.follower import FollowerEater
from ..pelican.repost   import RepostEater
from ..pelican.topic    import TopicEater

from helper import  Helper,\
                    worker_pelican,\
                    worker_shootup


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
    else:
        rtn = Helper.generate_listpage_resource(TopicUser,
                                                page,
                                                'name',
                                                '/topics/users')
    return dict(users=rtn['resource'], pagination=rtn['pagination'])


@route('/topics/weibos')
@route('/topics/weibos/<page:int>')
@view('topics/weibos')
def topics_weibos(page=0):
    user_id = request.query.get('user_id')
    if user_id:
        user_id = int(user_id)
        rtn = Helper.generate_listpage_resource(TopicWeibo,
                                                page,
                                                'content',
                                                '/topics/weibos',
                                                user_id=user_id)
    else:
        rtn = Helper.generate_listpage_resource(TopicWeibo,
                                                page,
                                                'content',
                                                '/topics/weibos')
    return dict(weibos=rtn['resource'], pagination=rtn['pagination'])


@get('/topics/new')
@view('topics/new')
def topics_new_show():
    pass


@post('/topics/new')
def topics_new_fetch():
    new_topic = request.forms.get('topic-name').decode('utf-8')
    Q.enqueue(worker_pelican, 'topic', new_topic)
    redirect('/topics')


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
    repost_id = request.query.get('repost_id')
    if repost_id:
        repost_id = int(repost_id)
        rtn = Helper.generate_listpage_resource(RepostUser,
                                                page,
                                                'name',
                                                '/reposts/users',
                                                repost_id=repost_id)
    else:
        rtn = Helper.generate_listpage_resource(RepostUser,
                                                page,
                                                'name',
                                                '/reposts/users')
    return dict(users=rtn['resource'], pagination=rtn['pagination'])


@get('/reposts/new')
@view('reposts/new')
def reposts_new_show():
    pass


@post('/reposts/new')
def reposts_new_fetch():
    repost_url = request.forms.get('weibo-url').decode('utf-8')
    Q.enqueue(worker_pelican, 'repost', repost_url)
    redirect('/reposts')


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
    bigv_id = request.query.get('bigv_id')
    if bigv_id:
        bigv_id = int(bigv_id)
        rtn = Helper.generate_listpage_resource(BigVFollower,
                                                page,
                                                'name',
                                                '/bigvs/followers',
                                                bigv_id=bigv_id)
    else:
        rtn = Helper.generate_listpage_resource(BigVFollower,
                                                page,
                                                'name',
                                                '/bigvs/followers')
    return dict(followers=rtn['resource'], pagination=rtn['pagination'])


@get('/bigvs/new')
@view('bigvs/new')
def bigvs_new_show():
    pass


@post('/bigvs/new')
def bigvs_new_fetch():
    weibo_id = request.forms.get('weibo-id').decode('utf-8')
    Q.enqueue(worker_pelican, 'follower', weibo_id)
    redirect('/bigvs')


@get('/im')
@view('im/im')
def im_show():
    weibo_ids_query = request.query.get('weibo_ids')
    if weibo_ids_query:
        weibo_ids = weibo_ids_query.decode('utf-8')
        return dict(weibo_ids=weibo_ids)
    else:
        return dict(weibo_ids=None)



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


@post('/fetch/topic/<topic_id:int>')
def topic_fetch(topic_id):
    topic = DB.query(Topic).filter_by(id=topic_id).first()
    Q.enqueue(worker_pelican, 'topic', topic.name)
    return {'result': 1}

@post('/pipeline/im')
def im_handler():
    weibo_ids_list = request.forms.get('weibo-ids').split(',')
    im_content = request.forms.get('im-content')
    Q.enqueue(worker_shootup, weibo_ids_list, im_content)
    redirect('/topics')

# Run Server
################################################
def run_server():
    run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    run_server()
