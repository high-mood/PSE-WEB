from influxdb import InfluxDBClient
from app.API import spotify


def add_genres(tracks, ids, access_token):
    artists_info = spotify.get_artists(access_token, ids)

    for artist_info in artists_info["artists"]:
        for track in tracks:
            if tracks[track]["fields"]["artistid"] != artist_info["id"]:
                continue

            tracks[track]["fields"]["genres"] = ",".join(artist_info["genres"])
            if not len(tracks[track]["fields"]["genres"]) > 0:
                tracks[track]["fields"]["genres"] = "None"


def add_audio_features(tracks, ids, access_token):
    features = spotify.get_audio_features(access_token, ids)

    for audio_features in features["audio_features"]:
        tracks[audio_features["id"]]["fields"]["duration_ms"] = audio_features["duration_ms"]
        tracks[audio_features["id"]]["fields"]["key"] = audio_features["key"]
        tracks[audio_features["id"]]["fields"]["mode"] = audio_features["mode"]
        tracks[audio_features["id"]]["fields"]["time_signature"] = audio_features["time_signature"]
        tracks[audio_features["id"]]["fields"]["acousticness"] = audio_features["acousticness"]
        tracks[audio_features["id"]]["fields"]["danceability"] = audio_features["danceability"]
        tracks[audio_features["id"]]["fields"]["energy"] = audio_features["energy"]
        tracks[audio_features["id"]]["fields"]["instrumentalness"] = float(audio_features["instrumentalness"])
        tracks[audio_features["id"]]["fields"]["liveness"] = audio_features["liveness"]
        tracks[audio_features["id"]]["fields"]["loudness"] = audio_features["loudness"]
        tracks[audio_features["id"]]["fields"]["speechiness"] = audio_features["speechiness"]
        tracks[audio_features["id"]]["fields"]["valence"] = audio_features["valence"]
        tracks[audio_features["id"]]["fields"]["tempo"] = audio_features["tempo"]


def get_latest_tracks(user_id, access_token):
    recently_played = spotify.get_recently_played(access_token)

    if not len(recently_played["items"]) > 0:
        return

    tracks = {}
    artists = []
    for track in recently_played["items"]:
        tracks[track["track"]["id"]] = {"measurement": user_id,
                                        "time": track["played_at"],
                                        "fields": {"songid": track["track"]["id"],
                                                   "artistid": track["track"]["artists"][0]["id"]}}
        # We only get the main artist
        artists.append(track["track"]["artists"][0]["id"])

    add_audio_features(tracks, list(tracks.keys()), access_token)
    add_genres(tracks, artists, access_token)

    return tracks


def update_user_tracks(access_token):
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('songs')

    user_id = spotify.get_user_info(access_token)["id"]
    print("getting data for " + user_id)

    tracks = get_latest_tracks(user_id, access_token)
    if tracks:
        print(list(tracks.values())[0]["measurement"])
        client.write_points(list(tracks.values()))
