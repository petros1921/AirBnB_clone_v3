#!/usr/bin/python3
"""Api THat handel a Review obj and operation."""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_place_by_id(place_id):
    """Reviw a place by id and return json of the reviews"""
    review_l = []
    pl_obj = storage.get("Place", str(place_id))

    if pl_obj is None:
        abort(404)

    for obj in pl_obj.reviews:
        review_l.append(obj.to_json())

    return jsonify(review_l)

@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_rev(place_id):
    """Returna a newly created review."""
    rev_json = request.get_json(silent=True)
    if rev_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", rev_json["user_id"]):
        abort(404)
    if "user_id" not in rev_json:
        abort(400, 'Missing user_id')
    if "text" not in rev_json:
        abort(400, 'Missing text')

    rev_json["place_id"] = place_id

    new_rev = Review(**rev_json)
    new_rev.save()
    responder = jsonify(new_rev.to_json())
    responder.status_code = 201

    return responder


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def reviews_id(review_id):
    """Retrive a specific review by id."""

    fet_obj = storage.get("Review", str(review_id))

    if fet_obj is None:
        abort(404)

    return jsonify(fet_obj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """Return a new review obj and 300 on suc and 404 on error."""
    pl_json = request.get_json(silent=True)

    if pl_json is None:
        abort(400, 'Not a JSON')

    fet_obj = storage.get("Review", str(review_id))

    if fet_obj is None:
        abort(404)

    for k, v in pl_json.items():
        if k not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(fet_obj, k, v)

    fet_obj.save()

    return jsonify(fet_obj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_reviby_id(review_id):
    """Delate a REview by id"""

    fet_obj = storage.get("Review", str(review_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
