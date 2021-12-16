#!/usr/bin/env python3

from cvt import create_address_by_pk
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/pk2addr/*":{"origins": "*"}})

def convert(prefix,pk):
    try:
        addr = create_address_by_pk(pk,prefix)
    except:
        addr = 'err'
    return addr

@app.route('/')
def index():
    return 'pubkey to address service, see <a href="https://plotnetwork.ltd">Plot Network Ltd</a> for more info'

@app.errorhandler(404)
def show_link(url):
    return '404 - page not found. this only intend to API usage'

@app.route('/pk2addr/<prefix>/<pk>')
def pk2addr(prefix,pk):
    return convert(prefix,pk)

@app.route('/pk2addr/<prefix>', methods=['POST'])
def pk2addrs(prefix):
    rd = request.get_json()
    res = {}
    if 'pks' in rd:
        addrs = []
        for pk in rd['pks']:
            addrs.append(convert(prefix,pk))
        res['addrs'] = addrs

    return jsonify(res)
