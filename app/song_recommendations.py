from time import sleep
from datetime import datetime
import requests
import sys
from app.API.spotify import get_access_token
from app.models import User
# from influxdb import InfluxDBClient

'''
Find recommendations given max 5 song ID's.
The recommendations are based on the given songs
and can be based on additional parameters for the given mood.
Parameters:
tracks    - list of given songs
token - oath token for spotify
Return
List of 5 tuple recommendations consisting of song id,
song name, main artist and playable link.
'''
def get_parameter_string(min_key=-1, min_mode=0,
                         min_acousticness=0.0, min_danceablility=0.0,
                         min_energy=0.0, min_instrumentalness=0.0,
                         min_liveness=0.0, min_loudness=-60,
                         min_speechiness=0.0, min_valence=0.0, min_tempo=0,
                         max_key=11, max_mode=1,
                         max_acousticness=1.0, max_danceablility=1.0,
                         max_energy=1.0, max_instrumentalness=1.0,
                         max_liveness=1.0, max_loudness=0,
                         max_speechiness=1.0, max_valence=1.0, max_tempo=99999):

    return (f"&min_key={min_key}&max_key={max_key}" +
            f"&min_mode={min_mode}&max_mode={max_mode}" +
            f"&min_acousticness={min_acousticness}&max_acousticness={max_acousticness}" +
            f"&min_danceablility={min_danceablility}&max_danceablility={max_danceablility}" +
            f"&min_energy={min_energy}&max_energy={max_energy}" +
            f"&min_instrumentalness={min_instrumentalness}&max_instrumentalness={max_instrumentalness}" +
            f"&min_liveness={min_liveness}&max_liveness={max_liveness}" +
            f"&min_loudness={min_loudness}&max_loudness={max_loudness}" +
            f"&min_speechiness={min_speechiness}&max_speechiness={max_speechiness}" +
            f"&min_valence={min_valence}&max_valence={max_valence}" +
            f"&min_tempo={min_tempo}&max_tempo={max_tempo}")


def find_song_recommendations(tracks, userid, recommendation_count, **params):
    tracks = tracks[:5]
    endpoint="https://api.spotify.com/v1/recommendations"
    track_string = '%2C'.join(tracks)
    token = get_access_token(User.get_refresh_token(userid))
    param_string = get_parameter_string(params)
    r = requests.get(f'{endpoint}?limit={recommendation_count}&seed_tracks={track_string}{param_string}', headers={"Authorization": "Bearer "+ token})
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        quit()

    song_recommendation = r.json()['tracks']
    recommendations = [{'songid': song['id'], 'name': song['name'], 'song_url': song['external_urls']['spotify'], 'artists': [artist['id'] for artist in song['artists']], 'image_url': song['album']['images'][0]['url']} for song in song_recommendation]
    return recommendations
