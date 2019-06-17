from sklearn.ensemble import GradientBoostingRegressor as GBR
from joblib import load
import numpy as np
import csv

''' Mood classification for server, requires the .joblib files imported hereunder.'''

def analyse_mood(songs):
    E_est = load('moodanalysis/Trained-Excitedness.joblib')
    H_est = load('moodanalysis/Trained-Happiness.joblib')
    features = ["mode", "time_signature", "acousticness",
                "danceability", "energy", "instrumentalness", "liveness", "loudness",
                "speechiness", "valence", "tempo"]
    input = []
    songtitles = []
    output = []
    if not songs:
        print('no songs found, quitting')
        return
    for song in songs:
        # Make list of titles.
        songtitles.append(song['fields']['songid'])
        # Make list matrix of inpudat data for algorithm.
        inputdata = []
        for feature in features:
            inputdata.append(song['fields'][feature])
        input.append(np.array([(100*x) for x in inputdata]))
    ExcitednessPredictions = E_est.predict(input)
    HappinessPredictions = H_est.predict(input)
    for i in range(len(songtitles)):
        outputdata = {}
        outputdata['songid'] = songtitles[i]
        outputdata['excitedness'] = ExcitednessPredictions[i]
        outputdata['happiness'] = HappinessPredictions[i]
        output.append(outputdata)
    return output
