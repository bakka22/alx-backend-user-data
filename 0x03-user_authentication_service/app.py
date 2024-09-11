#!/usr/bin/env python3
""" flask app module """
from flask import Flask, jsonify, request, make_response, abort
from flask import redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """ home page """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """ create a new user """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or password is None:
        abort(400)
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ log a user in """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or password is None:
        abort(400)
    if not AUTH.valid_login(email, password):
        abort(401)
    payload = {"email": f"{email}", "message": "logged in"}
    session_id = AUTH.create_session(email)
    response = make_response(jsonify(payload))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ log a user out """
    session_id = request.coockies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
