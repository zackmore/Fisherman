# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import os.path
import requests

from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..basket.basket import Topic, User, Weibo 

import pdb


class TopicEater(object):
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__),
                                    '../../config.json')
        with open(config_path) as config_file:
            config = json.load(config_file)
            self.token = config['pelican']['token'][0]
            self.entrance = config['pelican']['entrance']
            db_path = config['basket']['path']
            engine = create_engine(db_path)
            Session = sessionmaker(bind=engine)
            self.db = Session()

    def catch(self, topic):
        self.topic = urllib.quote_plus(topic)
        request_url = self.entrance % self.topic

        try:
            r = requests.get(request_url, headers=self.token)
        except e:
            print 'Network Error when requesting the %s:\n%s' % (request_url, e)
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

            # Processing all the pages
            for page in xrange(1, self.pages):
            #for page in xrange(1, 10):
                print '=========='
                print 'processing page %d' % page
                self._page_process(page)
                # TODO: time.sleep() randomly

    def _page_process(self, page_number):
        request_url = (self.entrance + config['pelican']['page_suffix']) % (
                        self.topic, page_number)

        try:
            r = requests.get(request_url, headers=self.token)
        except e:
            print 'Network Error when requesting the %s:\n%s' % (request_url, e) 
            sys.exit(1)

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

        topics = []
        weibo_content = weibo_tag.find(class_='ctt')
        links = weibo_content.find_all('a')

        if len(links) >= 1:
            for link in links:
                if re.search(config['helper']['topic_character'], link.get('href')):
                    if link.text not in topics:
                        topics.append(link.text)

        # save data
        for topic in topics:
            topic_instance = self.db.query(Topic).filter(Topic.name==topic).first()
            if topic_instance:
                data_topic = topic_instance
            else:
                data_topic = Topic(name=topic)

            user_instance = self.db.query(User).filter(User.link==user['link']).first()
            if user_instance:
                data_user = user_instance
            else:
                data_user = User(name=user['name'], link=user['link'])

            data_weibo = Weibo(content=weibo_content.text)
            data_user.weibos.append(data_weibo)

            data_topic.users.append(data_user)

            self.db.add(data_topic)
            self.db.commit()


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), '../../config.json')

    with open(config_path) as config_file:
        config = json.load(config_file)
        entrance = config['pelican']['entrance']

        test_topic = '#晨间日记#'
        pelican = TopicEater()
        pelican.catch(test_topic)
        #pdb.set_trace()
