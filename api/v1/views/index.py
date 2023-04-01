#!/usr/bin/python3
""" status of your api """

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def get_status():
    return jsonify({'status': 'OK'})
