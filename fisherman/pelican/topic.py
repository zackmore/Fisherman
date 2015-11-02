# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import os.path
import requests
import datetime
import random

from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..basket.basket import Topic, TopicUser, TopicWeibo 

import pdb


class TopicEater(object):
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__),
                                    '../../config.json')
        with open(config_path) as config_file:
            self.config = json.load(config_file)
            self.token = self.config['pelican']['token'][0]
            self.entrance = self.config['pelican']['topic_entrance']
            db_path = self.config['basket']['path']
            engine = create_engine(db_path)
            Session = sessionmaker(bind=engine)
            self.db = Session()

    def catch(self, topic):
        self.topic = urllib.quote_plus(topic.encode('utf-8'))
        request_url = self.entrance % self.topic

        try:
            r = requests.get(request_url, headers=self.token)
        except:
            print 'Network Error when requesting the %s' % request_url
            sys.exit(1)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            # Get pages
            inputs = soup.find_all('input', type='hidden')
            for input in inputs:
                if re.search('mp', input.decode()):
                    self.pages = int(input.get('value'))
                    break
                else:
                    continue

            # Get weibos_count
            weibos_count_text = soup.find(class_='cmt').text
            re_result = re.search('(?P<count>[0-9]+)', weibos_count_text)
            self.weibos_count = int(re_result.group('count'))

            # Processing all the pages
            for page in xrange(1, self.pages+1):
                print 'processing page %d' % page
                self._page_process(page)
                #time.sleep(random.randint(1, 10))
                time.sleep(random.randint(1, 3))
        else:
            print 'Could not login in'
            sys.exit(1)

    def _page_process(self, page_number):
        request_url = (self.entrance +
                        self.config['pelican']['topic_page_suffix']) % (
                        self.topic, page_number)

        try:
            r = requests.get(request_url, headers=self.token)
        except:
            print 'Network Error when requesting the %s' % request_url
            return False

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            # Get all weibos
            divs = soup.find_all('div', class_='c')
            weibos = [div for div in divs if re.search('M_', div.decode())]
            for weibo in weibos:
                self._weibo_process(weibo)

    def _weibo_process(self, weibo_tag):
        user = {}
        user['name'] = weibo_tag.find(class_='nk').text
        user['link'] = weibo_tag.find(class_='nk').get('href')
        come_from = weibo_tag.find(class_='ct').text
        come_keyword = '来自'
        start_point = come_from.find(come_keyword.decode('utf-8'))
        user['agent'] = come_from[start_point+2:]
        comment_link = weibo_tag.find_all(class_='cc')[-1].get('href')
        re_result = re.search('uid=(?P<uid>[0-9]+)\&', comment_link)
        if re_result:
            user['weibo_id'] = int(re_result.group('uid'))
        else:
            user['weibo_id'] = 0

        topics = []
        weibo_content = weibo_tag.find(class_='ctt')
        links = weibo_content.find_all('a')

        if len(links) >= 1:
            for link in links:
                if re.search(self.config['helper']['topic_character'],
                                link.get('href')):
                    if link.text not in topics:
                        topics.append(link.text)

        # save data
        for topic in topics:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Topic data
            topic_instance = self.db.query(Topic).\
                                filter(Topic.name==topic).\
                                first()
            if topic_instance:
                data_topic = topic_instance
            else:
                data_topic = Topic(name=topic)
                data_topic.created_at = now_time

            # Update current topic last_fetched_at, weibos_count
            if urllib.quote_plus(data_topic.name.encode('utf-8')) == self.topic:
                data_topic.last_fetched_at = now_time
                data_topic.weibos_count = self.weibos_count

            # User data
            user_instance = self.db.query(TopicUser).\
                                filter(TopicUser.link==user['link']).\
                                first()
            if user_instance:
                data_user = user_instance
            else:
                data_user = TopicUser(name=user['name'],
                                link=user['link'],
                                weibo_id=user['weibo_id'],
                                agent=user['agent'],
                                created_at=now_time)

            # Weibo data
            data_weibo = TopicWeibo(content=weibo_content.text,
                                    created_at=now_time)

            # Save
            data_user.topic_weibos.append(data_weibo)
            data_topic.topic_users.append(data_user)

            print data_topic

            #self.db.add(data_topic)
            #self.db.commit()


if __name__ == '__main__':
    onfig_path = os.path.join(os.path.dirname(__file__), '../../config.json')

    with open(config_path) as config_file:
        config = json.load(config_file)
        entrance = config['pelican']['topic_entrance']

        #test_topic = u'#晨间日记#'
        #test_topic = '#日记#'
        test_topic = u'#转发视奸#'
        pelican = TopicEater()
        pelican.catch(test_topic)
