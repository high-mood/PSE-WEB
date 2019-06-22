from flask import Flask, send_from_directory, jsonify, json, render_template, redirect, request, session, flash, url_for
from app import app
# Refactor later
from app import spotifysso
from app.utils import influx, spotify
from app.utils.tasks import update_user_tracks
from app.utils.models import User
from app.API.track_calls import TopSongs


@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    if "json_info" not in session:
        return render_template("login.html", **locals())
    else:

        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        userid = session['json_info']['id']
        access_token = spotify.get_access_token(session['json_info']['refresh_token'])
        all_songs = set(influx.get_songs(client, userid)[1])

        return render_template("index.html", **locals(), text=session['json_info']['display_name'],
                               id=session['json_info']['id'], song_history=all_songs)


@app.route("/index_js")
def index_js():
    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
    userid = session['json_info']['id']

    top_songs = influx.get_top_songs(client, userid, 10)
    timestamps, duration = influx.total_time_spent(client, userid)
    top_genres = influx.get_top_genres(client, userid, 10)

    # TODO these variables are not getting used.
    songs, song_count = [], []
    genres, genre_count = [], []
    if top_songs:
        songs, song_count = [list(x) for x in list(zip(*top_songs))]

    if top_genres:
        genres, genre_count = [list(x) for x in list(zip(*top_genres))]

    songs = TopSongs().get(userid, 10)['resource']['songs']
    print(songs)
    song_count = 10

    return render_template("index.js", songs=songs, song_count=song_count,
                           genres=genres, genre_count=genre_count,
                           timestamps=timestamps, duration=duration)


@app.route("/login")
def login():
    return spotifysso.authorize(callback=f"http://{app.config['HOST']}:5000/callback")


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
