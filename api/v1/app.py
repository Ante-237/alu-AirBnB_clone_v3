#!/usr/bin/python3
""" creating default route """

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')
app.url_map.strict_slashes = False
CORS(app, resources=r"/api/v1/*", origins="*")


host = os.getenv("HBNB_API_HOST", "0.0.0.0")
port = os.getenv("HBNB_API_PORT", 5000)


@app.teardown_appcontext
def teardown_storage(exception):
    """ closing storage """
    storage.close()


@app.errorhandler(404)
def error(self):
    """404 error but return empty dict"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """ just another flask app """
    app.run(host=host, port=port)
