"""
    views.py
    ~~~~~~~~~~~~
    This file contains the flask views that route URL's to functions. Primary functionality is the authentication of
    users.

    :copyright: 2019 Moodify (High-Mood)
    :authors:
           "Stan van den Broek",
           "Mitchell van den Bulk",
           "Mo Diallo",
           "Arthur van Eeden",
           "Elijah Erven",
           "Henok Ghebrenigus",
           "Jonas van der Ham",
           "Mounir El Kirafi",
           "Esmeralda Knaap",
           "Youri Reijne",
           "Siwa Sardjoemissier",
           "Barry de Vries",
           "Jelle Witsen Elias"
"""

import os

from flask import send_from_directory, render_template, redirect, request, session, flash, url_for

from app import app
# Refactor later
from app import spotifysso
from app.API.track_calls import TopSongs
from app.utils import influx, spotify
from app.utils.models import User, Song
from app.utils.tasks import update_user_tracks


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    if "json_info" not in session:
        return render_template("index.html", **locals())
    else:

        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        userid = session['json_info']['id']
        access_token = spotify.get_access_token(session['json_info']['refresh_token'])
        all_songs = set([Song.get_song_name(song['songid']) for song in influx.get_songs(client, userid)])

        return render_template("dashboard.html", **locals(), text=session['json_info']['display_name'],
                               id=session['json_info']['id'], song_history=all_songs)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/index_js")
def index_js():
    userid = session['json_info']['id']
    songs = TopSongs().get(userid, 10)['resource']['songs']
    song_count = 10

    return render_template("index.js", songs=songs, song_count=song_count, genres=[], genre_count=[], timestamps=[],
                           duration=[])


@app.route("/login")
def login():
    return spotifysso.authorize(callback=f"http://{app.config['HOST']}/callback")


@app.route('/callback')
def authorized():
    if "json_info" in session:
        return redirect(url_for("index"))

    resp = spotifysso.authorized_response()

    if resp is None:
        flash(f"Access denied: {request.args['error']}", 'error')
        return redirect(url_for('index'))
    if isinstance(resp, Exception):
        flash(f"Access denied: error={str(resp)}", 'error')
        return redirect(url_for('index'))

    access_token = resp['access_token']
    refresh_token = resp['refresh_token']
    # TODO dynamic scopes
    scopes = resp['scope'].split(" ")

    json_user_info = spotify.get_user_info(access_token)
    User.create_if_not_exist(json_user_info, refresh_token)  # TODO Add access token
    session['json_info'] = json_user_info  # TODO change this laziness
    session['json_info']['refresh_token'] = refresh_token

    update_user_tracks(access_token)

    return redirect(url_for('index'))


@app.route('/logout')
def sign_out():
    session.pop("json_info")

    return redirect(url_for('index'))
