#!/usr/bin/env python3
""" flask app module """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
