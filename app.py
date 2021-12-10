#!/usr/bin/env python3

from cvt import create_address_by_pk
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'pubkey to address service'

@app.route('/pk2addr/<prefix>/<pk>')
def pk2addr(prefix,pk):
    return create_address_by_pk(pk,prefix)

