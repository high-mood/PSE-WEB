from flask import send_from_directory, jsonify, json, render_template, redirect, request, session, flash, url_for
from app import app
from app import db
# Refactor later
from app import models
from app import spotifysso
from app.API import spotify


@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    if "json_info" not in session:
        return redirect(url_for("login"))
    else:
        return render_template("index.html", **locals())


@app.route("/login")
def login():
    return spotifysso.authorize(callback="http://localhost:5000/callback")
    # return spotifysso.authorize(callback=url_for('authorized', _external=True, _scheme="https"))


@app.route('/callback')
def authorized():
    resp = spotifysso.authorized_response()

    # TODO: EXception handling (if exception or if None#)
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, Exception):
        return 'Access denied: error=%s' % str(resp)

    access_token = resp['access_token']
    refresh_token = resp['refresh_token']
    scopes = resp['scope'].split(" ")

    json_user_info = spotify.get_user_info(access_token)
    models.User.create_if_not_exist(json_user_info, refresh_token)  # TODO Add access token
    session['json_info'] = json_user_info  # TODO change this laziness

    return redirect(url_for('index'))
