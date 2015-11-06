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

import pdb


class MessageMachinegun(object):
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__),
                                    '../../config.json')
        with open(config_path) as config_file:
            self.config = json.load(config_file)
            self.entrance = self.config['pipeline']['entrance']
            self.token = self.config['pelican']['token'][0]

    def _aim(self, weibo_id):
        url = self.entrance % weibo_id

        try:
            r = requests.get(url, headers=self.token)
        except:
            print 'Network Error when requesting the %s' % url
            sys.exit(1)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            form_tag = soup.find('form')
            self.form = {
                u'url': 'https://weibo.cn' + form_tag.get('action'),
                u'form_data': {
                    u'content': ''
                }
            }
            hidden_inputs = form_tag.find_all('input', type='hidden')
            for input_tag in hidden_inputs:
                self.form['form_data'][input_tag.get('name')] = input_tag.get('value')
        else:
            print 'Could not login in'
            sys.exit(1)

    def shoot(self, weibo_id, message):
        self._aim(weibo_id)
        self.form['form_data']['content'] = message

        try:
            r = requests.post(self.form['url'],
                                headers=self.token,
                                data=self.form['form_data'])
        except:
            print 'Network Error when send the im'
            sys.exit(1)

        if r:
            print '%s is down' % weibo_id

    def shootup(self, weibo_id_list, message):
        for weibo_id in weibo_id_list:
            self.shoot(weibo_id, message)


if __name__ == '__main__':
    machinegun = MessageMachinegun()
    machinegun.shoot('1651755490', '你好七啊')
