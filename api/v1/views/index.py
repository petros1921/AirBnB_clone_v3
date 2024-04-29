#!/usr/bin/python3

"""This is an index api."""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """return a json for statuse"""
    data = {
        "status": "OK"
    }

    responder = jsonify(data)
    responder.status_code = 200

    return responder

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """return a status with an obj with all"""
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    responder = jsonify(data)
    responder.status_code = 200

    return responder
