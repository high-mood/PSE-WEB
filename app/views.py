from flask import render_template, redirect, request, session, url_for
from app import app
# Refactor later
from app import spotifysso
from app.API import spotify, influx
from app.tasks import update_user_tracks


# TODO: Remove this later

@app.route("/test")
def indexer():
    return render_template("dashboard.html", **locals())


@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    if "json_info" not in session:
        return render_template("login.html", **locals())
    else:
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        userid = session['json_info']['id']
        access_token = spotify.get_access_token(session['json_info']['refresh_token'])

        recently_played = spotify.get_recently_played(access_token)
        top_songs = influx.get_top_songs(client, userid, 10, access_token)
        top_genres = influx.get_top_genres(client, userid, 10)
        all_genres = influx.get_genres(client, userid)
        total_listening_time = influx.total_time_spent(client, userid)

        # print(type(recently_played))
        # print(type(top_songs))
        # print(type(top_genres))
        # print(type(all_genres))
        # print(type(total_listening_time))
        # print(session['json_info'])
        return render_template("index.html", **locals(), text=session['json_info']['display_name'],
                               id=session['json_info']['id'])


@app.route("/index_js")
def index_js():
    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
    userid = session['json_info']['id']
    access_token = spotify.get_access_token(session['json_info']['refresh_token'])

    top_songs = influx.get_top_songs(client, userid, 10, access_token)
    timestamps, duration = influx.total_time_spent(client, userid)
    top_genres = influx.get_top_genres(client, userid, 10)
    duration = [time / 60000 for time in duration]
    songs, song_count = [list(x) for x in list(zip(*top_songs))]
    genres, genre_count = [list(x) for x in list(zip(*top_genres))]

    return render_template("index.js", songs=songs, song_count=song_count,
                           genres=genres, genre_count=genre_count,
                           timestamps=timestamps, duration=duration)


@app.route("/login")
def login():
    return spotifysso.authorize(callback=f"http://{app.config['HOST']}:5000/callback")

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
    # models.User.create_if_not_exist(json_user_info, refresh_token)  # TODO Add access token
    session['json_info'] = json_user_info  # TODO change this laziness
    session['json_info']['refresh_token'] = refresh_token

    update_user_tracks(access_token)

    return redirect(url_for('index'))
