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

from ..basket.basket import RepostWeibo, RepostUser

import pdb


class RepostEater(object):
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

    def catch(self, url):
        base_url_o = urlparse.urlparse(url)
        self.base_url = base_url_o[0] + '://' + base_url_o[1] + base_url_o[2]

        try:
            r = requests.get(self.base_url, headers=self.token)
        except:
            print 'Network Error when requesting the %s' % self.base_url
            sys.exit(1)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            # Get content
            self.content = soup.find(class_='ctt').text

            # Get pages
            inputs = soup.find_all('input', type='hidden')
            for input in inputs:
                if re.search('mp', input.decode()):
                    self.pages = int(input.get('value'))
                    break
                else:
                    continue

            # Get repost count
            repost_text = soup.find(id='rt').text
            re_result = re.search('\[(?P<repost_count>[0-9]*)\]', repost_text)
            self.repost_count = re_result.group('repost_count')

            # Formating the RepostWeibo
            repost_weibo_instance = self.db.query(RepostWeibo).\
                                filter(RepostWeibo.base_url==self.base_url).\
                                first()

            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if repost_weibo_instance:
                self.repost_weibo = repost_weibo_instance
                self.repost_weibo.last_fetched_at = now_time
            else:
                self.repost_weibo = RepostWeibo(base_url=self.base_url,
                                                content=self.content,
                                                repost_count=self.repost_count,
                                                created_at=now_time,
                                                last_fetched_at=now_time)

            # Processing all the pages
            for page in xrange(1, self.pages+1):
                print 'processing page %s' % page
                if not self._page_process(page):
                    continue
                time.sleep(random.randint(1, 10))
        else:
            print 'Could not login in'
            sys.exit(1)

    def _page_process(self, page):
        request_url = self.base_url + '?&page=%s' % page

        try:
            r = requests.get(request_url, headers=self.token)
        except:
            print 'Network Error when requesting the %s' % request_url
            return False

        if r.status_code == 200:
            print 'ok'
            soup = BeautifulSoup(r.text, 'html.parser')

            # Get all weibos
            all_content_divs = soup.find_all('div', class_='c')
            reposts = [div for div in all_content_divs\
                            if div.find('span', class_='cc')]
            for repost in reposts:
                self._repost_process(repost)

                # Save
                self.db.add(self.repost_weibo)
                self.db.commit()
        else:
            print 'Could not fetch url: %s' % request_url
            return False

    def _repost_process(self, repost):
        user_tag = repost.find_all('a')[0]
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        user = {}
        user['name'] = user_tag.text
        user['link'] = user_tag.get('href')
        come_from = repost.find(class_='ct').text
        come_keyword = '来自'
        start_point = come_from.find(come_keyword.decode('utf-8'))
        user['agent'] = come_from[start_point+2:]
        re_result = re.search('/u/(?P<uid>[0-9]+)$', user['link'])
        if re_result:
            user['weibo_id'] = int(re_result.group('uid'))
        else:
            try:
                r = requests.get('https://weibo.cn' + user['link'],
                                    headers=self.token)
            except:
                user['weibo_id'] = 0

            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                user_tag = soup.find('div', class_='u')
                link = user_tag.find_all('a')[0].get('href')

                re_result = re.search('/(?P<uid>[0-9]+)/', link)
                if re_result:
                    user['weibo_id'] = int(re_result.group('uid'))
                else:
                    user['weibo_id'] = 000
            else:
                user['weibo_id'] = 00

        #####
        user['created_at'] = now_time

        self.repost_weibo.repost_users.append(RepostUser(
                                                name=user['name'],
                                                link=user['link'],
                                                agent=user['agent'],
                                                weibo_id=user['weibo_id'],
                                                created_at=user['created_at']))


if __name__ == '__main__':
    url = 'https://weibo.cn/repost/CEF36dVY7?uid=1810274375&rl=0'
    pelican = RepostEater()
    pelican.catch(url)
