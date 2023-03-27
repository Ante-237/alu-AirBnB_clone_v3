#!/usr/bin/python3
""" list of states """
from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def cities_by_states():
    """ working with cities and states """
    states_list = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states_list)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ just some quick teardown """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
