# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import urlparse
import os.path
import requests
import datetime
import random

from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..basket.basket import BigV, BigVFollower

import pdb


class FollowerEater(object):
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__),
                                    '../../config.json')
        with open(config_path) as config_file:
            self.config = json.load(config_file)
            self.token = self.config['pelican']['token'][0]
            db_path = self.config['basket']['path']
            engine = create_engine(db_path)
            Session = sessionmaker(bind=engine)
            self.db = Session()

    def _process_bigv(self):
        bigv_url = self.config['pelican']['follower_link'] % self.weibo_id

        try:
            r = requests.get(bigv_url, headers=self.token)
        except:
            print 'Network Error when requesting the %s' % bigv_url
            sys.exit(1)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            bigv_instance = self.db.query(BigV).\
                                filter(BigV.weibo_id==self.weibo_id).\
                                first()
            if bigv_instance:
                bigv = bigv_instance
                bigv.last_fetched_at = now_time
            else:
                bigv = BigV(weibo_id=self.weibo_id)
                bigv.created_at = now_time
                bigv.link = bigv_url

                bigv_tag = soup.find('div', class_='u')
                include_name_text = bigv_tag.find('span', class_='ctt').text
                include_name_text = include_name_text.replace(u'\xa0', ' ')
                bigv.name = include_name_text.split(' ')[0]
                bigv.last_fetched_at = now_time

                self.bigv = bigv
                return True
        else:
            print 'Status_code is %s' % r.status_code
            return False

    def _process_bigv_followers(self):
        follower_url = self.config['pelican']['follower_entrace'] %\
                        (self.weibo_id, 1)

        try:
            r = requests.get(follower_url, headers=self.token)
        except:
            print 'Network Error when requesting the %s' % follower_url
            sys.exit(1)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            # Process Followers Pages
            hidden_tag = soup.find_all('input', type='hidden')[-1]
            self.pages = int(hidden_tag.get('value'))

            for page in xrange(1, self.pages+1):
                print 'processing page %s' % page
                if not self._process_page(page):
                    continue
                time.sleep(random.randint(1, 3))
        else:
            print 'Could not login in'
            sys.exit(1)

    def _process_page(self, page):
        url = self.config['pelican']['follower_entrace'] % (self.weibo_id, page)

        try:
            r = requests.get(url, headers=self.token)
        except:
            print 'Network Error when requesting the %s' % url
            return False

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            users_tags = soup.find_all('table')

            if users_tags:
                for tag in users_tags:
                    link = tag.find('a').get('href')
                    if not self._process_follower(link, tag):
                        continue
            else:
                print 'No User Data in %s' % url
                return False
        else:
            print 'Status_code is %s' % r.status_code
            return False

    def _process_follower(self, user_url, tag):
        try:
            r = requests.get(user_url, headers=self.token)
        except:
            print 'Network Error when requesting the %s' % user_url
            return False

        if r.status_code == 200:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            follower_instance = self.db.query(BigVFollower).\
                                filter(BigVFollower.link==user_url).\
                                first()
            if follower_instance:
                follower = follower_instance
            else:
                follower = BigVFollower(link=user_url)
                follower.created_at = now_time
                follower.name = tag.find_all('a')[1].text
                follow_href = tag.find_all('a')[-1].get('href')
                re_result = re.search('uid=(?P<uid>[0-9]+)&', follow_href)
                follower.weibo_id = re_result.group('uid')

                self.bigv.bigv_followers.append(follower)
        else:
            return False

    def catch(self, weibo_id):
        self.weibo_id = weibo_id

        if self._process_bigv():
            self._process_bigv_followers()

            self.db.add(self.bigv)
            self.db.commit()
        else:
            print 'Could not get bigv'
            sys.exit(1)



if __name__ == '__main__':
    url = '2120244897'
    pelican = FollowerEater()
    pelican.catch(url)
