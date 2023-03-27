#!/usr/bin/python3
""" working with default routes
    python is cool"""
from flask import Flask
from flask import render_template
from markupsafe import Markup
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
    return "C {}".format(takeout)


@app.route('/python/')
@app.route('/python/<text>')
def pythonR(text='is cool'):
    """ python is cool """
    takeout = text.replace("_", " ")
    return "Python {}".format(takeout)


@app.route('/number/<int:n>')
def number(n):
    """ work for numbers only """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>')
def templateNumber(n):
    """ display template if only integer """
    n = Markup.escape(n)
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    # """ everything starts here """
    app.run(host="0.0.0.0", port=5000, debug=True)
