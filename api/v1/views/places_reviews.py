#!/usr/bin/python3
"""new view for RESTful api actions"""

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.review import Review
from api.v1.views import app_views
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_allreviews(place_id):
    ''' reviews'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews), 200


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''creating review'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in review_data:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, review_data['user_id'])
    if not user:
        abort(404)
    if 'text' not in review_data:
        return jsonify({'error': 'Missing text'}), 400
    review_data['place_id'] = place_id
    review = Review(**review_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def reviews_actions(review_id):
    ''' review action for all'''
    if request.method == 'GET':
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        return jsonify(review.to_dict()), 200

    if request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        review_data = request.get_json()
        if not review_data:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in review_data.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200