from datetime import datetime
from app.utils import influx, spotify
import numpy as np
from app import db
from moodanalysis.moodAnalysis import analyse_mood
from app.utils.models import User, Song, Artist, Songmood
from app import app
import sys
from scipy.spatial import distance
import operator


def add_artist_genres(artist_ids, access_token):
    """
    Adds the artist with there genres to the SQL database.
    :param artist_ids: List of artist ids.
    :param access_token: A valid access token from the Spotify Accounts service.
    """
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
    """
    Adds the tracks with there audio features to the SQL database.
    :param tracks: List of track ids.
    :param access_token: A valid access token from the Spotify Accounts service.
    :return: A list of audio features per song to be able to do mood analysis later.
    """
    if not tracks:
        return
    track_ids = list(tracks.keys())
    audio_features = spotify.get_audio_features(access_token, track_ids)

    spotify_features = ['duration_ms', 'key', 'mode', 'time_signature', 'acousticness',
                        'danceability', 'energy', 'instrumentalness', 'liveness',
                        'loudness', 'speechiness', 'valence', 'tempo']

    tracks_features = []
    for i, features in enumerate(audio_features['audio_features']):
        track_features = {'songid': track_ids[i]}
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
            'songid': track_features['songid'],
            'name': tracks[track_features['songid']]['name'],
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
    """
    Updates the mean excitedness and happiness for the user with there songs in the last `duration`.
    :param duration: Duration to generate mean mood for (i.e. 1h, 1d, 1w etc).
    :param userid: Spotify user id of the user.
    """
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
    mean_excitedness = 0
    mean_happiness = 0
    for mood in moods:
        mean_excitedness += mood.excitedness
        mean_happiness += mood.happiness

    data = [{'measurement': userid,
             'time': f"'{datetime.now().isoformat()}Z'",
             'fields': {
                 'excitedness': mean_excitedness / song_count,
                 'happiness': mean_happiness / song_count,
                 'songcount': song_count
             }}]

    client.switch_database('moods')
    client.write_points(data)

    print(f'[{current_time}] updated moods for {userid}')


def get_latest_tracks(user_id, access_token):
    """
    Gets the 50 most recent tracks from that the user listened to and stores multiple aspects of them.
    :param user_id: Spotify user id of the user.
    :param access_token: A valid access token from the Spotify Accounts service.
    :return: The 50 most recent tracks for the timescale database and there audio features for mood analysis.
    """
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
        # 'artistsids': ','.join([artist['songid'] for artist in track['track']['artists']])}
        artists[track['track']['artists'][0]['id']] = None
        tracks[track['track']['id']] = {'name': track['track']['name']}

    print('\ntracks', tracks)
    tracks_features = add_audio_features(tracks, access_token)
    print('\nfeatures', tracks_features)
    add_artist_genres(artists, access_token)

    return latest_tracks, tracks_features


def update_user_tracks(access_token):
    """
    Gets the latest tracks the user listened to and updates the databases accordingly.
    :param access_token: A valid access token from the Spotify Accounts service.
    """
    user_data = spotify.get_user_info(access_token)
    tracks, tracks_features = get_latest_tracks(user_data['id'], access_token)

    # If the user does not have listened to any tracks we just skip them.
    current_time = datetime.now().strftime("%H:%M:%S")

    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
    if tracks:
        update_songmoods(tracks_features)
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
    :param tracks: dict of tracks formatted as: {'songid': {'name': 'actual song name'}}
    :return: list of dictionaries containing features and mood per song.
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
    features_moods = link_features_mood(tracks)

    return features_moods


def link_features_mood(tracks=None):
    """Link features and moods for tracks or all tracks in db if tracks=none."""
    if tracks:
        results = db.session.query(Songmood, Song).join(Song, Song.songid == Songmood.songid).filter(Song.songid.in_((tracks.keys()))).all()
    else:
        results = db.session.query(Songmood, Song).join(Song, Song.songid == Songmood.songid)
    features_moods = []
    for mood, song in results:
        print(mood, song)
        features_moods.append({
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
        })
    return features_moods


def update_song_features(tracks):
    """
    Update the song features for the given tracks.
    :param tracks: dict of tracks formatted as: {'songid': {'name': 'actual song name'}}
    """
    songs = db.session.query(Song).filter(Song.songid.in_((tracks.keys()))).all()
    found_ids = [song.songid for song in songs]
    not_found_ids = [song_id for song_id in tracks.keys() if song_id not in found_ids]
    new_tracks = {}

    for song_id in not_found_ids:
        new_tracks[song_id] = tracks[song_id]

    # TODO don't hardcode 'snipy12'
    refresh_token = User.get_refresh_token('snipy12')
    access_token = spotify.get_access_token(refresh_token)
    add_audio_features(new_tracks, access_token)


def order_songs(songs, target, n=5):
    """
    It orders songs based on Euclidean distance of the target and recommended songs mood
    :param songs: list of dicts formatted as: [{'songid' : actual song id, excitedness: actual excitedness, happiness: actual happiness}].
    :param target: the target mood formatted as: (excitedness, happiness).
    :param n: the amount of recommendations that are returned.
    :return: ascending list of n dictionaries formatted as: [{'songid' : actual song id, excitedness: actual excitedness, happiness: actual happiness}].
    """
    # Adds the Euclidean distance to the dictionaries and sorts the list in ascending order.
    for song in songs:
        song['distance'] = distance.euclidean(target, (song['excitedness'], song['happiness']))

    ordered_songs = sorted(songs, key=lambda k: k['distance'])

    # Removes the distance from the dictionaries and returns the best n tracks.
    for d in ordered_songs:
        del d['distance']

    return ordered_songs[:n]


def _get_parameter_string(min_key=-1, min_mode=0,
                          min_acousticness=0.0, min_danceablility=0.0,
                          min_energy=0.0, min_instrumentalness=0.0,
                          min_liveness=0.0, min_loudness=-60,
                          min_speechiness=0.0, min_valence=0.0, min_tempo=0,
                          max_key=11, max_mode=1,
                          max_acousticness=1.0, max_danceablility=1.0,
                          max_energy=1.0, max_instrumentalness=1.0,
                          max_liveness=1.0, max_loudness=0,
                          max_speechiness=1.0, max_valence=1.0, max_tempo=99999):
    """ Fills in emtpy parameters with their default value. """
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


def find_song_recommendations(tracks, userid, recommendation_count=20, target=(0.0, 0.0), **params):
    """
    Find recommendations given max 5 song ID's.
    The recommendations are based on the given songs and can be based on additional parameters for the given mood.
    :param tracks: list of given songs.
    :param userid: Spotify user id of the user.
    :param recommendation_count: Amount of recommendations
    :param target: the target mood formatted as: (excitedness, happiness).
    :param params: Audio feature parameters.
    :return: List of given amount of recommendations as a list of dictionaries of song ids and moods.
    """
    tracks = tracks[:5]
    track_string = '%2C'.join(tracks)
    access_token = spotify.get_access_token(User.get_refresh_token(userid))
    param_string = _get_parameter_string(**params)
    response = spotify.get_recommendations(access_token, recommendation_count, track_string, param_string)

    song_recommendation = response['tracks']
    recommendations = {song['id']: {'name': song['name']} for song in song_recommendation}
    moods = get_features_moods(recommendations)
    top5 = order_songs(moods, target)
    return top5
