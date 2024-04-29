#!/usr/bin/python3
"""A place and amenities linker."""

from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def place_amin(place_id):
    """Return the aminities presented with and id"""
    fet_obj = storage.get("Place", str(place_id))

    total_amni = []

    if fet_obj is None:
        abort(404)

    for obj in fet_obj.amenities:
        total_amni.append(obj.to_json())

    return jsonify(total_amni)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def amenity_unlink(place_id, amenity_id):
    """Unlink an aminity with the placer and return an error"""
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    fet_obj = storage.get("Place", place_id)
    found = 0

    for obj in fet_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fet_obj.amenities.remove(obj)
            else:
                fet_obj.amenity_ids.remove(obj.id)
            fet_obj.save()
            found = 1
            break

    if found == 0:
        abort(404)
    else:
        responder = jsonify({})
        responder.status_code = 201
        return responder


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def amenity_link(place_id, amenity_id):
    """REturn an Aminity and place linkeed or 404 on error"""

    fet_obj = storage.get("Place", str(place_id))
    am_obj = storage.get("Amenity", str(amenity_id))
    amenity_fn = None

    if not fet_obj or not am_obj:
        abort(404)

    for obj in fet_obj.amenities:
        if str(obj.id) == amenity_id:
            amenity_fn = obj
            break

    if amenity_fn is not None:
        return jsonify(amenity_fn.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fet_obj.amenities.append(am_obj)
    else:
        fet_obj.amenities = am_obj

    fet_obj.save()

    responder = jsonify(am_obj.to_json())
    responder.status_code = 201

    return responder
