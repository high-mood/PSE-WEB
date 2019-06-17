from datetime import datetime
from app.API import spotify, influx
import numpy as np
from app import db
from moodanalysis.moodAnalysis import analyse_mood
from app.models import Song, Artist, Songmood
from app import app
import sys


def add_artist_genres(artist_ids, access_token):
    if not artist_ids:
        return
    artists_info = spotify.get_artists(access_token, list(artist_ids.keys()))

    for artist_info in artists_info['artists']:
        Artist.create_if_not_exist({
            'artistid': artist_info['id'],
            'name': artist_info['name'],
            'genres': ', '.join(artist_info['genres']),
            'popularity': artist_info['popularity']
        })


def add_audio_features(tracks, access_token):
    if not tracks:
        return
    track_ids = list(tracks.keys())
    audio_features = spotify.get_audio_features(access_token, track_ids)

    spotify_features = ['duration_ms', 'key', 'mode', 'time_signature', 'acousticness',
                        'danceability', 'energy', 'instrumentalness', 'liveness',
                        'loudness', 'speechiness', 'valence', 'tempo']

    tracks_features = []
    for i, features in enumerate(audio_features['audio_features']):
        track_features = {'id': track_ids[i]}
        for feature in spotify_features:
            # Some songs do not have audio_features.
            if not audio_features:
                track_features[feature] = None
            else:
                # We explicitly cast these to the sure there are no type conflicts in our database.
                track_features[feature] = float(features[feature])
        # We only add it to the return data if the track has features.
        if track_features['danceability']:
            tracks_features.append(track_features)

        Song.create_if_not_exist({
            'songid': track_features['id'],
            'name': tracks[track_features['id']]['name'],
            'duration_ms': track_features['duration_ms'],
            'key': track_features['key'],
            'mode': track_features['mode'],
            'time_signature': track_features['time_signature'],
            'acousticness': track_features['acousticness'],
            'danceability': track_features['danceability'],
            'energy': track_features['energy'],
            'instrumentalness': track_features['instrumentalness'],
            'liveness': track_features['liveness'],
            'loudness': track_features['loudness'],
            'speechiness': track_features['speechiness'],
            'valence': track_features['valence'],
            'tempo': track_features['tempo']
        })

    return tracks_features


def get_last_n_minutes(duration, userid):
    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
    client.switch_database('songs')

    song_history = client.query(f'select songid from \"{userid}\" where time > now()-{duration}').raw

    current_time = datetime.now().strftime("%H:%M:%S")

    if 'series' not in song_history:
        print(f'[{current_time}] no recent history found for {userid} in the last {duration}')
        return
    else:
        song_history = song_history['series'][0]['values']

    _, songids = list(zip(*song_history))
    moods = Songmood.get_moods(songids)

    if not moods:
        print(f'[{current_time}] no moods found for {userid}')
        return

    song_count = len(moods)
    excitedness, happiness = list(zip(*moods))
    excitedness_mean = np.mean(excitedness)
    happiness_mean = np.mean(happiness)

    # songcount = len(songids)
    # excitedness = np.random.uniform(-10, 10)
    # happiness = np.random.uniform(-10, 10)

    data = [{'measurement': userid,
             'time': datetime.now().isoformat(),
             'fields': {
                 'excitedness': excitedness_mean,
                 'happiness': happiness_mean,
                 'songcount': song_count
             }}]

    client.switch_database('moods')
    client.write_points(data)

    print(f'[{current_time}] updated moods for {userid}')


def get_latest_tracks(user_id, access_token):
    recently_played = spotify.get_recently_played(access_token)

    if not len(recently_played['items']) > 0:
        return None, None

    tracks = {}
    artists = {}
    latest_tracks = []
    for track in recently_played['items']:
        latest_tracks.append({'measurement': user_id,
                              'time': track['played_at'],
                              'fields': {'songid': track['track']['id']}})
        # 'artistsids': ','.join([artist['id'] for artist in track['track']['artists']])}
        artists[track['track']['artists'][0]['id']] = None
        tracks[track['track']['id']] = {'name': track['track']['name']}

    track_features = add_audio_features(tracks, access_token)
    add_artist_genres(artists, access_token)

    return latest_tracks, track_features


def update_user_tracks(access_token):
    user_data = spotify.get_user_info(access_token)
    tracks, track_features = get_latest_tracks(user_data['id'], access_token)

    # If the user does not have listened to any tracks we just skip them.
    current_time = datetime.now().strftime("%H:%M:%S")

    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
    if tracks:
        querystring = '(' + ','.join([f"'{track['fields']['songid']}'" for track in tracks]) + ');'
        duplicates = [x[0] for x in db.session.query('songid FROM songmoods where songid in ' + querystring)]
        analysis_tracks = [track for track in track_features if track['id'] not in duplicates]

        if analysis_tracks:
            moods = analyse_mood(analysis_tracks)
            for mood in moods:
                Songmood.create_if_not_exist(mood)

        client.write_points(tracks)
        print(f"[{current_time}] Succesfully stored the data for '{user_data['display_name']}'")
    else:
        print(f"[{current_time}] Could not find any tracks for '{user_data['display_name']}', skipping",
              file=sys.stderr)
