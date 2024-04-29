#!/usr/bin/python3
""" Index """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """Retuen atwo num obj for each of them."""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    objects_num = {}
    for index in range(len(classes)):
        objects_num[names[index]] = storage.count(classes[index])

    return jsonify(objects_num)
