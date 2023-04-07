#!/usr/bin/python3
"""new view for RESTful api actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_allplaces(city_id):
    ''' get places in storage'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''create places from struct'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_data = request.get_json()
    if not place_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in place_data:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, place_data['user_id'])
    if not user:
        abort(404)
    if 'name' not in place_data:
        return jsonify({'error': 'Missing name'}), 400
    place_data['city_id'] = city_id
    place = Place(**place_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places_actions(place_id):
    '''action on all places'''
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        return jsonify(place.to_dict()), 200

    if request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        place_data = request.get_json()
        if not place_data:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in place_data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200