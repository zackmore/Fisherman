# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import os.path
import requests
import sqlalchemy
from bs4 import BeautifulSoup

import pdb


class TopicEater(object):
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__),
                                    '../../config.json')
        with open(config_path) as config_file:
            config = json.load(config_file)
            self.token = config['pelican']['token'][0]
            self.entrance = config['pelican']['entrance']
            self.basket = config['basket']['path']

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
            for page in xrange(1, self.pages + 1):
                self._page_process(page)

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
                # TODO: time.sleep() randomly

    def _weibo_process(self, weibo_tag):
        user = {}
        user['name'] = weibo_tag.find(class_='nk').text
        user['link'] = weibo_tag.find(class_='nk').get('href')

        topics_links = []
        weibo_content = weibo_tag.find(class_='ctt')
        links = weibo_content.find_all('a')

        if len(links) >= 1:
            for link in links:
                if re.search(config['helper']['topic_character'], link.get('href')):
                    if link.text not in topics_links:
                        topics_links.append(link.text)

        # TODO: save data
        pdb.set_trace()



if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), '../../config.json')

    with open(config_path) as config_file:
        config = json.load(config_file)
        entrance = config['pelican']['entrance']

        test_topic = '#晨间日记#'
        pelican = TopicEater()
        pelican.catch(test_topic)
        #pelican = TopicEater(config['pelican']['entrance'])
