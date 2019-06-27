"""
    mood_analysis.py
    ~~~~~~~~~~~~
    This file conducts mood analysis. It utilizes a gradient-boosting regressor to analyze spotify parameters
    and convert this into a mood.

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

import sys

import numpy as np
from joblib import load


def analyse_mood(songs):
    """
    Mood classification, requires the .joblib files imported hereunder.
    :param songs: List of songs with features
    :return: List of songs with classified excitedness and happiness.
    """
    h_est = load('moodanalysis/Trained-Happiness.joblib')
    e_est = load('moodanalysis/Trained-Excitedness.joblib')
    features = ["mode", "time_signature", "acousticness", "danceability",
                "energy", "instrumentalness", "liveness", "loudness",
                "speechiness", "valence", "tempo"]
    if not songs:
        print('no songs found, quitting', file=sys.stderr)
        return

    input_data = []
    song_titles = []
    to_be_skipped = []
    for i, song in enumerate(songs):
        # Store song titles to return the later.
        song_titles.append(song['songid'])
        if not song['danceability']:
            to_be_skipped.append(i)
        else:
            # Make list matrix of input data for algorithm.
            input_data.append(np.array([song[feature] for feature in features]))

    output = []
    songs_skipped = 0
    happiness_predictions = h_est.predict(input_data)
    excitedness_predictions = e_est.predict(input_data)
    for i in range(len(songs)):
        if i in to_be_skipped:
            output_data = {'songid': song_titles[i],
                           'happiness': None,
                           'excitedness': None}
            songs_skipped += 1
        else:
            output_data = {'songid': song_titles[i],
                           'happiness': float(happiness_predictions[i - songs_skipped]),
                           'excitedness': float(excitedness_predictions[i - songs_skipped])}
        output.append(output_data)

    return output
