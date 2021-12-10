#!/usr/bin/env python3

from cvt import create_address_by_pk
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'pubkey to address service, see <a href="https://plotnetwork.ltd">Plot Network Ltd</a> for more info'

@app.errorhandler(404)
def show_link():
    return '404 - page not found. this only intend to API usage'

@app.route('/pk2addr/<prefix>/<pk>')
def pk2addr(prefix,pk):
    try:
        addr = create_address_by_pk(pk,prefix)
    except:
        addr = 'err'
    return addr


