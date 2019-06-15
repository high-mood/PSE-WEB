from datetime import datetime
from app.API import spotify, influx
import numpy as np
from app import db
from moodanalysis.moodAnalysis import analyse_mood
from app.models import Song, Artist, Songmood
from app import app
import sys


def add_genres(tracks, ids, access_token):
    if not ids:
        return
    artists_info = spotify.get_artists(access_token, ids)

    for artist_info in artists_info['artists']:
        Artist.create_if_not_exist({'artistid': artist_info['id'],
                                    'name': artist_info['name'],
                                    'genres': ', '.join(artist_info['genres']),
                                    'popularity': artist_info['popularity']})

        for track in tracks:
            if track['fields']['artistsids'].split(',')[0] != artist_info['id']:
                continue

            track['fields']['genres'] = ','.join(artist_info['genres'])

    for track in tracks:
        if 'genres' not in track['fields'] or not len(track['fields']['genres']) > 0:
            track['fields']['genres'] = "None"


def add_audio_features(tracks, ids, access_token):
    if not ids:
        return
    features = spotify.get_audio_features(access_token, ids)

    for audio_features in features['audio_features']:
        for track in tracks:
            if track['fields']['songid'] != audio_features['id']:
                continue
            # We explicitly cast these to the sure there are no type conflicts in our database.
            track['fields']['duration_ms'] = int(audio_features['duration_ms'])
            track['fields']['key'] = int(audio_features['key'])
            track['fields']['mode'] = int(audio_features['mode'])
            track['fields']['time_signature'] = int(audio_features['time_signature'])
            track['fields']['acousticness'] = float(audio_features['acousticness'])
            track['fields']['danceability'] = float(audio_features['danceability'])
            track['fields']['energy'] = float(audio_features['energy'])
            track['fields']['instrumentalness'] = float(audio_features['instrumentalness'])
            track['fields']['liveness'] = float(audio_features['liveness'])
            track['fields']['loudness'] = float(audio_features['loudness'])
            track['fields']['speechiness'] = float(audio_features['speechiness'])
            track['fields']['valence'] = float(audio_features['valence'])
            track['fields']['tempo'] = float(audio_features['tempo'])


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


def get_latest_tracks(user_id, access_token):
    recently_played = spotify.get_recently_played(access_token)

    if not len(recently_played['items']) > 0:
        return

    tracks = []
    trackids = {}
    artistids = {}
    # print(recently_played['items'][0]['track']['name'])
    for track in recently_played['items']:
        Song.create_if_not_exist({'songid': track['track']['id'],
                                  'name': track['track']['name']
                                  })
        tracks.append({'measurement': user_id,
                       'time': track['played_at'],
                       'fields': {'songid': track['track']['id'],
                                  'artistsids': ','.join([artist['id'] for artist in track['track']['artists']])
                                  }
                       })
        # We store the artist and track ids in dics to
        # prefent requesting them multiple time from Spotify.
        # We only get the genre from the main artist
        artistids[track['track']['artists'][0]['id']] = 0
        trackids[track['track']['id']] = 0

    add_audio_features(tracks, list(trackids.keys()), access_token)
    add_genres(tracks, list(artistids.keys()), access_token)

    return tracks


def update_user_tracks(access_token):
    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])

    user_data = spotify.get_user_info(access_token)

    tracks = get_latest_tracks(user_data['id'], access_token)

    # If the user does not have listened to any tracks we just skip them.
    current_time = datetime.now().strftime("%H:%M:%S")
    
    if tracks:
        querystring = '(' + ','.join([f"'{track['fields']['songid']}'" for track in tracks]) + ');'
        duplicates = [x[0] for x in db.session.query('songid FROM songmoods where songid in ' + querystring)]
        analysis_tracks = [track for track in tracks if track['fields']['songid'] not in duplicates]

        if analysis_tracks:
            moods = analyse_mood(analysis_tracks)
            print(moods)
            for mood in moods:
                Songmood.create_if_not_exist(mood)

        client.write_points(tracks)
        print(f"[{current_time}] Succesfully stored the data for '{user_data['display_name']}'")
    else:
        print(f"[{current_time}] Could not find any tracks for '{user_data['display_name']}', skipping",
              file=sys.stderr)
