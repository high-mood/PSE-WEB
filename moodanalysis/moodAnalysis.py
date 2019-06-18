from joblib import load
import numpy as np
import sys


def analyse_mood(songs):
    """
    Mood classification, requires the .joblib files imported hereunder.
    :param songs: List of songs with features
    :return: List of songs with classified excitedness and happiness.
    """
    e_est = load('moodanalysis/Trained-Excitedness.joblib')
    h_est = load('moodanalysis/Trained-Happiness.joblib')
    features = ["mode", "time_signature", "acousticness", "danceability",
                "energy", "instrumentalness", "liveness", "loudness",
                "speechiness", "valence", "tempo"]
    if not songs:
        print('no songs found, quitting', file=sys.stderr)
        return

    input_data = []
    song_titles = []
    for song in songs:
        if not song['key']:
            continue
        # Store song titles to return the later.
        song_titles.append(song['id'])
        # Make list matrix of input data for algorithm.
        input_data.append(np.array([(100 * song[feature]) for feature in features]))

    output = []
    excitedness_predictions = e_est.predict(input_data)
    happiness_predictions = h_est.predict(input_data)
    for i in range(len(song_titles)):
        output_data = {'songid': song_titles[i],
                       'excitedness': float(excitedness_predictions[i]) / 100,
                       'happiness': float(happiness_predictions[i]) / 100}
        output.append(output_data)

    return output
