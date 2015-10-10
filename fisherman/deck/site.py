# -*- coding: utf-8 -*-

from bottle import route, run, template, static_file

@route('/')
def homepage():
    return template('base')

@route('/hello/<name>')
def index(name):
    return template('<strong>{{ name }}</strong>', name=name)

@route('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root='./static/')


run(host='localhost', port=8080, reloader=True)
