#!/usr/bin/python3
"""an Api for cities"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_by_id(state_id):
    """Return a json fill for all the citis or 404 for error."""
    list_city = []
    st_obj = storage.get("State", state_id)

    if st_obj is None:
        abort(404)
    for obj in st_obj.cities:
        list_city.append(obj.to_json())

    return jsonify(list_city)

@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """This will Reeturn a newly created id."""
    json_ci = request.get_json(silent=True)
    if json_ci is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in json_ci:
        abort(400, 'Missing name')

    json_ci["state_id"] = state_id

    added_city = City(**city_json)
    added_city.save()
    responder = jsonify(added_city.to_json())
    responder.status_code = 201

    return responder

@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_id(city_id):
    """This will Return a specific id for a city obj and it will creat an."""

    fet_obj = storage.get("City", str(city_id))

    if fet_obj is None:
        abort(404)

    return jsonify(fet_obj.to_json())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """Return a City obj in 200 on a success and 400 or 404 on failure"""
    ci_json = request.get_json(silent=True)
    if ci_json is None:
        abort(400, 'Not a JSON')
    fet_obj = storage.get("City", str(city_id))
    if fet_obj is None:
        abort(404)
    for k, v in ci_json.items():
        if k not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fet_obj, k, v)
    fet_obj.save()
    return jsonify(fet_obj.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_id_del(city_id):
    """Delete a city by id."""

    fet_obj = storage.get("City", str(city_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
