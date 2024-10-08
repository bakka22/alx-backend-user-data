#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv("AUTH_TYPE", None)
auth_dict = {"auth": Auth, "basic_auth": BasicAuth,
             "session_auth": SessionAuth}
if auth_type:
    auth = auth_dict.get(auth_type)
    if auth:
        auth = auth()


@app.before_request
def before_req():
    """ handle events before every request """
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']
    if auth is None:
        return
    s_auth = auth.session_cookie(request)
    request.current_user = auth.current_user(request)
    if auth.require_auth(request.path, excluded_paths):
        if auth.authorization_header(request) is None and s_auth is None:
            abort(401)
        elif request.current_user is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unautherized(error) -> str:
    """ unautherized error """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ unautherized error """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
