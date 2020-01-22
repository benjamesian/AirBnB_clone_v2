#!/usr/bin/python3
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(error):
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    selected_states = storage.all(State)
    if id is not None:
        selected_states = list(filter(lambda x: x.id == id, selected_states))
    return render_template('9-states.html', id=id, states=selected_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
