from influxdb import InfluxDBClient
from app.API import spotify
import numpy as np


def add_genres(tracks, ids, access_token):
    artists_info = spotify.get_artists(access_token, ids)

    for artist_info in artists_info["artists"]:
        for track in tracks:
            if tracks[track]["tags"]["artistid"] != artist_info["id"]:
                continue
            try:
                tracks[track]["fields"]["genres"] = artist_info["genres"][0]
            except IndexError:
                tracks[track]["fields"]["genres"] = "None"


def add_audio_features(tracks, ids, access_token):
    features = spotify.get_audio_features(access_token, ids)

    for audio_features in features["audio_features"]:
        feature_set = {"duration_ms": audio_features["duration_ms"],
                       "key": audio_features["key"],
                       "mode": audio_features["mode"],
                       "time_signature": audio_features["time_signature"],
                       "acousticness": audio_features["acousticness"],
                       "danceability": audio_features["danceability"],
                       "energy": audio_features["energy"],
                       "instrumentalness": audio_features["instrumentalness"],
                       "liveness": audio_features["liveness"],
                       "loudness": audio_features["loudness"],
                       "speechiness": audio_features["speechiness"],
                       "valence": audio_features["valence"],
                       "tempo": audio_features["tempo"]}

        tracks[audio_features["id"]]["fields"] = feature_set


def get_latest_tracks(user_id, access_token):
    recently_played = spotify.get_recently_played(access_token)

    if not len(recently_played["items"]) > 0:
        return

    tracks = {}
    artists = []
    for track in recently_played["items"]:
        tracks[track["track"]["id"]] = {"measurement": user_id,
                                        "time": track["played_at"],
                                        "tags": {"songid": track["track"]["id"],
                                                 "artistid": track["track"]["artists"][0]["id"]}}

        artists.append(track["track"]["artists"][0]["id"])

    add_audio_features(tracks, ",".join(tracks.keys()), access_token)
    add_genres(tracks, ",".join(artists), access_token)

    return tracks


def update_user_tracks(access_token):
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('songs')

    user_id = spotify.get_user_info(access_token)

    stuff = get_latest_tracks(user_id, access_token)

    client.write_points(list(stuff.values()))
