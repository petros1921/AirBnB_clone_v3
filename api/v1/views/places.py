#!/usr/bin/python3
"""An API That handle Place object"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)

def place_city_by_id(city_id):
    """This will Return a place json"""
    place_lists = []
    c_obj = storage.get("City", str(city_id))
    for obj in c_obj.places:
        place_lists.append(obj.to_json())

    return jsonify(place_lists)

@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """THis will handel a newly created place"""
    pl_json = request.get_json(silent=True)
    if pl_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", pl_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in pl_json:
        abort(400, 'Missing user_id')
    if "name" not in pl_json:
        abort(400, 'Missing name')

    pl_json["city_id"] = city_id

    new_p = Place(**pl_json)
    new_p.save()
    responder = jsonify(new_p.to_json())
    responder.status_code = 201

    return responder

@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)

def places_id(place_id):
    """Return a place obj with a specified id or 404"""

    fet_obj = storage.get("Place", str(place_id))

    if fet_obj is None:
        abort(404)

    return jsonify(fet_obj.to_json())

@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """Return a place obj and 200 on suc and 404 on error"""
    pl_json = request.get_json(silent=True)

    if pl_json is None:
        abort(400, 'Not a JSON')

    fet_obj = storage.get("Place", str(place_id))

    if fet_obj is None:
        abort(404)

    for k, v in pl_json.items():
        if k not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fet_obj, k, v)

    fet_obj.save()

    return jsonify(fet_obj.to_json())

@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_placeby_id(place_id):
    """This will delate a  place by id."""

    fet_obj = storage.get("Place", str(place_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
