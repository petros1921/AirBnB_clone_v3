#!/usr/bin/python3
"""An app Module that starts a Flask web application."""

from os import getenv
from flask import Flask, jsonify
from models import storage

from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(exception):
    """Function that Closes the storage"""
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """handle an error that is 404."""
    data = {
        "error": "Not found"
    }

    responder = jsonify(data)
    responder.status_code = 404

    return(responder)

if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
