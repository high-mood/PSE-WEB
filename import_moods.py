"""
    import_moods.py
    ~~~~~~~~~~~~
    This file can be utilized to query the Influx database to get
    songs and their Spotify parameters.

    :copyright: 2019 Moodify (High-Mood)
    :authors:
           "Stan van den Broek",
           "Mitchell van den Bulk",
           "Mo Diallo",
           "Arthur van Eeden",
           "Elijah Erven",
           "Henok Ghebrenigus",
           "Jonas van der Ham",
           "Mounir El Kirafi",
           "Esmeralda Knaap",
           "Youri Reijne",
           "Siwa Sardjoemissier",
           "Barry de Vries",
           "Jelle Witsen Elias"
"""

from app import app
from app import db
from app.utils import influx
from app.utils.models import Song, Songmood
from moodanalysis.moodAnalysis import analyse_mood

if __name__ == "__main__":
    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
    client.switch_database('songs')
    all_data = client.query('select "songid"  from /.*/').raw['series']
    all_values = [data['values'] for data in all_data]
    flattened_data = [x for sublist in all_values for x in sublist]
    data = [x[1] for x in flattened_data]
    types = ["acousticness", "danceability", "duration_ms", "energy", "instrumentalness", "key", "liveness", "loudness",
             "mode", "songid", "speechiness", "tempo", "time_signature", "valence"]
    features = db.session.query(Song).filter(Song.songid.in_(data)).all()
    tracks = []
    for f in features:
        tracks.append({
            'songid': f.songid,
            'duration_ms': f.duration_ms,
            'key': f.key,
            'mode': f.mode,
            'time_signature': f.time_signature,
            'acousticness': f.acousticness,
            'danceability': f.danceability,
            'energy': f.energy,
            'instrumentalness': f.instrumentalness,
            'liveness': f.liveness,
            'loudness': f.loudness,
            'speechiness': f.speechiness,
            'valence': f.valence,
            'tempo': f.tempo
        })

    moods = analyse_mood(tracks)

    for data in moods:
        data['response_count'] = 0
        data['response_excitedness'] = 0.0
        data['response_happiness'] = 0.0
        Songmood.create_if_not_exist(data)
