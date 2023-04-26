#!/usr/bin/python3
""" status of your api """


from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.user import User
from models.place import Place
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def get_status():
    """ RETURN JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_count():
    """ count number state """
    classes = {
        Amenity: "amenities",
        City: "cities",
        Place: "places",
        Review: "reviews",
        State: "states",
        User: "users"
    }
    return jsonify({name: storage.count(cls) for cls, name in classes.items()})
