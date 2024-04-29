#!/usr/bin/python3
"""This will handel the states of the obj and opertation"""

from api.v1.views import app_views, storage
from models.state import State
from flask import jsonify, abort, request

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get():
    """Return a state list in the json."""
    s_list= []
    obj_st = storage.all("State")
    for obj in obj_st.values():
        s_list.append(obj.to_json())

    return jsonify(state_list)

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """This will creat an obj state."""
    st_json = request.get_json(silent=True)
    if st_json is None:
        abort(400, 'Not a JSON')
    if "name" not in st_json:
        abort(400, 'Missing name')

    n_state = State(**st_json)
    n_state.save()
    responder = jsonify(n_state.to_json())
    responder.status_code = 201

    return responder

@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_with_id(state_id):
    """Return a state obj with a specific id or with error"""

    fet_obj = storage.get("State", str(state_id))

    if fet_obj is None:
        abort(404)

    return jsonify(fet_obj.to_json())

@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """Return a state obj and 200 on success, or 400 on failure."""
    st_json = request.get_json(silent=True)
    if st_json is None:
        abort(400, 'Not a JSON')
    fet_obj = storage.get("State", str(state_id))
    if fet_obj is None:
        abort(404)
    for k, v in st_json.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(fet_obj, k, v)
    fet_obj.save()
    return jsonify(fet_obj.to_json())

@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_del(state_id):
    """Delates  astate by ID."""

    fet_obj = storage.get("State", str(state_id))

    if fet_obj is None:
        abort(404)
    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
