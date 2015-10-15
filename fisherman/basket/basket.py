# -*- coding: utf-8 -*-

import sys
import json
import os.path
import subprocess
import sqlalchemy

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

import pdb


Base = declarative_base()

class Topic(Base):
    __tablename__ = 'topics'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    last_fetched_at = Column(String, default=None)
    name = Column(String)
    weibos_count = Column(Integer)
    created_at = Column(String)

    def __repr__(self):
        return '<Topic(name="%s")>' % self.name.encode('utf-8')


class User(Base):
    __tablename__ = 'topic_users'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    weibo_id = Column(Integer)
    name = Column(String)
    link = Column(String)
    agent = Column(String)
    created_at = Column(String)
    topic_id = Column(Integer, ForeignKey('topics.id'))

    topic = relationship('Topic', backref=backref('topic_users', order_by=id))

    def __repr__(self):
        return '<User(name="%s", link="%s")>' % (self.name.encode('utf-8'), self.link)


class Weibo(Base):
    __tablename__ = 'topic_weibos'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(String)
    user_id = Column(Integer, ForeignKey('topic_users.id'))

    user = relationship('User', backref=backref('topic_weibos', order_by=id))

    def __repr__(self):
        return '<Weibo(content="%s")>' % (self.content.encode('utf-8'))


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__),
                                '../../config.json')
    with open(config_path) as config_file:
        config = json.load(config_file)
        db_path = config['basket']['path']

    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
