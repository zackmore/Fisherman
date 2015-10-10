# -*- coding: utf-8 -*-

import sys
import json
import os.path
import subprocess
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import pdb


Base = declarative_base()

class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return '<Topic(name="%s")>' % self.name


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)

    def __repr__(self):
        return '<User(name="%s", link="%s")>' % (self.name, self.link)


class Weibo(Base):
    __tablename__ = 'weibos'

    id = Column(Integer, primary_key=True)
    content = Column(String)

    def _repr__(self):
        return '<Weibo(content="%s")>' % (self.content)


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__),
                                '../../config.json')
    with open(config_path) as config_file:
        config = json.load(config_file)
        db_path = 'sqlite:///' + os.path.join(os.path.dirname(__file__),
                                    config['basket']['path'])
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
