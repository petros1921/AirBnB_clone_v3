#!/usr/bin/python3
"""Aminity Restful Api action handlers for every aminity."""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Gets all amenities list."""
    amin_list = []
    amin_obj = storage.all("Amenity")
    for obj in amin_obj.values():
        amin_list.append(obj.to_json())

    return jsonify(amin_list)

@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """This will creat an aminity and obj."""
    amin_json = request.get_json(silent=True)
    if amin_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amin_json:
        abort(400, 'Missing name')

    new_amin = Amenity(**amin_json)
    new_amin.save()
    responder = jsonify(new_amin.to_json())
    responder.status_code = 201

    return responder

@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
def id_amenity(amenity_id):
    """Return an amenity to the dict."""
    fet_obj = storage.get("Amenity", str(amenity_id))

    if fet_obj is None:
        abort(404)

    return jsonify(fet_obj.to_json())

@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """This will update an aminity in it instance"""
    amin_json = request.get_json(silent=True)
    if amin_json is None:
        abort(400, 'Not a JSON')
    fet_obj = storage.get("Amenity", str(amenity_id))
    if fet_obj is None:
        abort(404)
    for k, v in amin_json.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(fet_obj, k, v)
    fet_obj.save()
    return jsonify(fet_obj.to_json())



@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)

def delete_amenity(amenity_id):
    """Delat an aminity in the param by the id."""
    fet_obj = storage.get("Amenity", str(amenity_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
