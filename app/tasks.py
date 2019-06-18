from datetime import datetime
from app.API import spotify, influx
import numpy as np
from app import db
from moodanalysis.moodAnalysis import analyse_mood
from app.models import User, Song, Artist, Songmood
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

    print('\ntracks', tracks)
    track_features = add_audio_features(tracks, access_token)
    print('\nfeatures', track_features)
    add_artist_genres(artists, access_token)

    return latest_tracks, track_features


def update_user_tracks(access_token):
    user_data = spotify.get_user_info(access_token)
    tracks, track_features = get_latest_tracks(user_data['id'], access_token)

    # If the user does not have listened to any tracks we just skip them.
    current_time = datetime.now().strftime("%H:%M:%S")

    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
    if tracks:
        update_songmoods(track_features)
        client.write_points(tracks)
        print(f"[{current_time}] Succesfully stored the data for '{user_data['display_name']}'")
    else:
        print(f"[{current_time}] Could not find any tracks for '{user_data['display_name']}', skipping",
              file=sys.stderr)


def update_songmoods(tracks_features):
    songids = [track['songid'] for track in tracks_features]
    songmoods = db.session.query(Songmood).filter(Songmood.songid.in_((songids))).all()
    found_ids = [songmood.songid for songmood in songmoods]
    analysis_tracks = [track for track in tracks_features if track['songid'] not in found_ids]

    if analysis_tracks:
        moods = analyse_mood(analysis_tracks)
        for mood in moods:
            Songmood.create_if_not_exist(mood)


def get_features_moods(tracks):
    """
    Gather all audio features and moods for given tracks.
    :param tracks - dict of tracks format: {'songid': {
                                                'name': 'actual song name'
                                                }
                                           }
    :return list of dictionaries containing features and mood per song.
    """
    update_song_features(tracks)
    songs = db.session.query(Song).filter(Song.songid.in_((tracks.keys()))).all()
    tracks_features = []
    for song in songs:
        tracks_features.append(
            {
                'songid': song.songid,
                'name': song.name,
                'duration_ms': song.duration_ms,
                'key': song.key,
                'mode': song.mode,
                'time_signature': song.time_signature,
                'acousticness': song.acousticness,
                'danceability': song.danceability,
                'energy': song.energy,
                'instrumentalness': song.instrumentalness,
                'liveness': song.liveness,
                'loudness': song.loudness,
                'speechiness': song.speechiness,
                'valence': song.valence,
                'tempo': song.tempo
            })
    update_songmoods(tracks_features)

    result = db.session.query(Songmood, Song).join(Song, Song.songid == Songmood.songid)
    moods_features = []
    for mood, feature in result:
        moods_features = {
            'songid': mood.songid,
            'excitedness': mood.excitedness,
            'happiness': mood.happiness,
            'name': song.name,
            'duration_ms': song.duration_ms,
            'key': song.key,
            'mode': song.mode,
            'time_signature': song.time_signature,
            'acousticness': song.acousticness,
            'danceability': song.danceability,
            'energy': song.energy,
            'instrumentalness': song.instrumentalness,
            'liveness': song.liveness,
            'loudness': song.loudness,
            'speechiness': song.speechiness,
            'valence': song.valence,
            'tempo': song.tempo
        }
    return moods_features


def update_song_features(tracks):
    songs = db.session.query(Song).filter(Song.songid.in_((tracks.keys()))).all()
    found_ids = [song.songid for song in songs]
    not_found_ids = [id for id in tracks.keys() if id not in found_ids]
    new_tracks = {}

    for songid in not_found_ids:
        new_tracks[songid] = tracks[songid]

    # TODO
    refresh_token = User.get_refresh_token('snipy12')
    access_token = spotify.get_access_token(refresh_token)
    add_audio_features(new_tracks, access_token)
