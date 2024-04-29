#!/usr/bin/python3
"""API that handels athe user objective"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_user():
    """Gets the user objective abd return json of all users"""
    lists = []
    users = storage.all("User")
    for obj in users.values():
        lists.append(obj.to_json())

    return jsonify(lists)

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Return newly created user"""
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    responder = jsonify(new_user.to_json())
    responder.status_code = 201

    return responder

@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_id(user_id):
    """Retrive a user id"""

    fet_obj = storage.get("User", str(user_id))

    if fet_obj is None:
        abort(404)

    return jsonify(fet_obj.to_json())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """Update a specific user obj and return 200 on sucess and 404 not"""
    u_json = request.get_json(silent=True)

    if u_json is None:
        abort(400, 'Not a JSON')

    fet_obj = storage.get("User", str(user_id))

    if fet_obj is None:
        abort(404)

    for k, v in u_json.items():
        if k not in ["id", "created_at", "updated_at", "email"]:
            setattr(fet_obj, k, v)

    fet_obj.save()

    return jsonify(fet_obj.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def delete_userby_id(user_id):
    """DElates a user by id"""

    fet_obj = storage.get("User", str(user_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
