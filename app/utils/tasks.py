from app.utils.models import User, Song, Artist, Songmood, SongArtist
from moodanalysis.moodAnalysis import analyse_mood
from app.utils import influx, spotify
from app import app
from app import db

from datetime import datetime
import sys


def add_artist_genres(artist_ids, access_token):
    """
    Adds the artist with there genres to the SQL database.
    :param artist_ids: List of artist ids.
    :param access_token: A valid access token from the Spotify Accounts service.
    """
    if not artist_ids:
        return
    # The list of artists can be larger then 50, which is the limit of artists you can request to Spotify, so
    # we split the artists up in chunks of maximum 50 artists.
    n = 50
    keys_list = list(artist_ids.keys())
    artist_ids_chunks = [keys_list[i * n:(i + 1) * n] for i in range((len(keys_list) + n - 1) // n)]
    for artist_ids_list in artist_ids_chunks:
        artists_info = spotify.get_artists(access_token, artist_ids_list)

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


def add_song_artist_link(song_artist_links):
    """
    Add the link between artist and song the SQL database.
    :param song_artist_links: List of dicts structured like [{'songid': songid, 'artistid': artistid}, ]
    """
    for link in song_artist_links:
        SongArtist.create_if_not_exist(link)


def get_latest_tracks(user_id, access_token):
    """
    Gets the 50 most recent tracks from that the user listened to and stores multiple aspects of them.
    :param user_id: Spotify user id of the user.
    :param access_token: A valid access token from the Spotify Accounts service.
    :return: The 50 most recent tracks for the timescale database and there audio features for mood analysis.
    """
    recently_played = spotify.get_recently_played(access_token)

    if not recently_played['items']:
        return None, None

    tracks = {}
    artists = {}
    latest_tracks = []
    track_artist_link = []
    for track in recently_played['items']:
        latest_tracks.append({'measurement': user_id,
                              'time': track['played_at'],
                              'fields': {'songid': track['track']['id']}})
        # We add the track and artist ids to dicts to remove duplicates.
        for artist in track['track']['artists']:
            artists[artist['id']] = None
            track_artist_link.append({'songid': track['track']['id'],
                                      'artistid': artist['id']})
        tracks[track['track']['id']] = {'name': track['track']['name']}

    tracks_features = add_audio_features(tracks, access_token)
    add_artist_genres(artists, access_token)
    add_song_artist_link(track_artist_link)

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
        print(f"[{current_time}] Successfully stored the data for '{user_data['display_name']}'")
    else:
        print(f"[{current_time}] Could not find any tracks for '{user_data['display_name']}', skipping",
              file=sys.stderr)


def get_last_n_minutes(duration, userid):
    """
    Updates the mean excitedness and happiness for the user with there songs in the last `duration`.
    :param duration: Duration to generate mean mood for (i.e. 1h, 1d, 1w etc).
    :param userid: Spotify user id of the user.
    """
    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
    client.switch_database('songs')

    song_history = influx.get_songs(client, userid, duration=duration)

    current_time = datetime.now().strftime("%H:%M:%S")

    if not song_history:
        print(f'[{current_time}] no recent history found for {userid} in the last {duration}')
        return

    moods = Songmood.get_moods([song['songid'] for song in song_history])

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


def update_songmoods(tracks_features):
    """
    Updates songmoods.
    :param tracks_features: List of tracks features.
    """
    songids = [track['songid'] for track in tracks_features]
    songmoods = Songmood.get_moods(songids)
    found_ids = [songmood.songid for songmood in songmoods]
    analysis_tracks = [track for track in tracks_features if track['songid'] not in found_ids]

    if analysis_tracks:
        moods = analyse_mood(analysis_tracks)
        for mood in moods:
            mood['response_count'] = 0
            mood['response_excitedness'] = 0.0
            mood['response_happiness'] = 0.0
            Songmood.create_if_not_exist(mood)


def get_features_moods(tracks):
    """
    Gather all audio features and moods for given tracks.
    :param tracks: dict of tracks formatted as: {'songid': {'name': 'actual song name'}}
    :return: list of dictionaries containing features and mood per song.
    """
    update_song_features(tracks)
    songs = Song.get_songs(tracks.keys())
    tracks_features = []
    for song in songs:
        tracks_features.append({
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


def link_features_mood(tracks=None, get_responses=False):
    """Link features and moods for tracks or all tracks in db if tracks=none."""
    if tracks:
        results = Song.get_songs_with_mood(tracks.keys())
    elif get_responses:
        results = Song.get_all_songs_with_mood_if_responses()
    else:
        results = Song.get_all_songs_with_mood()

    features_moods = []
    for mood, song in results:
        features_moods.append({
            'songid': mood.songid,
            'excitedness': mood.excitedness,
            'happiness': mood.happiness,
            'response_excitedness': mood.response_excitedness,
            'response_happiness': mood.response_happiness,
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
    songs = Song.get_songs(tracks.keys())
    found_ids = [song.songid for song in songs]
    not_found_ids = [song_id for song_id in tracks.keys() if song_id not in found_ids]
    new_tracks = {}

    for song_id in not_found_ids:
        new_tracks[song_id] = tracks[song_id]

    # TODO don't hardcode 'snipy12'
    refresh_token = User.get_refresh_token('snipy12')
    access_token = spotify.get_access_token(refresh_token)
    add_audio_features(new_tracks, access_token)
