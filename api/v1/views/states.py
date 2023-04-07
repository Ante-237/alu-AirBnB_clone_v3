#!/usr/bin/python3
"""create a new view for State objects"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, make_response


@app_views.route('/states', methods=['GET', ], strict_slashes=False)
def get_states():
    """return the list of states"""
    states = storage.all(State).values()  # get all states
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    data = request.get_json()
    if not data:
        return jsonify({'error': "Not a JSON"}), 400
    name = data.get('name', None)
    if not name:
        return jsonify({'error': "Missing name"}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_id(state_id):
    """return the list of states"""
    state = storage.get(State, state_id)

    if not state:
        status = 404
        return jsonify({'error': "Not found"}), status

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        status = 200
        return jsonify({}), status

    if request.method == 'GET':
        return jsonify(state.to_dict()), 200

    if request.method == 'PUT':
        if not request.get_json():
            return jsonify({'error': "Not a JSON"}), 400
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        status = 200

        return jsonify(state.to_dict()), status
