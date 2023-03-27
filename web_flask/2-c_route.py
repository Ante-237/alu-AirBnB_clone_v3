#!/usr/bin/python3
# working with flask:x
""" moving to end points  """
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def home():
    """ default home route """
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """  hbnb end point """
    return "HBNB"


@app.route("/c/<text>")
def info_c(text):
    """ taking argument for displaying c """
    takeout = text.replace("_", " ")
    return 'C {}'.format(takeout)


if __name__ == '__main__':
    # """ everything starts here """
    app.run(host="0.0.0.0", port=5000, debug=True)
