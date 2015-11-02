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
        pagination['current'] = current_page
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


def worker_pelican(pelican_type, entrance):
    if pelican_type == 'topic':
        pelican = TopicEater()
    elif pelican_type == 'follower':
        pelican = FollowerEater()
    elif pelican_type == 'repost':
        pelican = RepostEater()

    pelican.catch(entrance)
