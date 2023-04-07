#!/usr/bin/python3
"""new view for RESTful API actions"""

from flask import abort, request, jsonify
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """retrieve all users"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def create_user():
    '''create user'''
    # users = storage.all(User).values()
    user_data = request.get_json()
    if not user_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in user_data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in user_data:
        return jsonify({'error': 'Missing password'}), 400
    user_data.pop('id', None)
    user_data.pop('created_at', None)
    user_data.pop('updated_at', None)
    user = User(**user_data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>/', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_user(user_id):
    """user actions"""
    if request.method == 'GET':
        """get user"""
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict()), 200

    if request.method == 'DELETE':
        """delete user"""
        users = storage.get(User, user_id)
        if not users:
            abort(404)
        storage.delete(users)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        """ update user"""
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        user_data = request.get_json()
        if not user_data:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in user_data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
