from sklearn.ensemble import GradientBoostingClassifier as GBC
from joblib import load
import numpy as np

''' Mood classification for server, requires the .joblib files imported hereunder.'''

E_est = load('moodanalysis/Trained-Excitedness.joblib')
H_est = load('moodanalysis/Trained-Happiness.joblib')
features = ["mode", "time_signature", "acousticness",
        "danceability", "energy", "instrumentalness", "liveness", "loudness",
        "speechiness", "valence", "tempo"]

def analyse_mood(songs):
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
        input.append(inputdata)
    for val in input:
        print(val)
    ExcitednessPredictions = E_est.predict(input)
    HappinessPredictions = H_est.predict(input)
    for i in range(len(songtitles)):
        print(ExcitednessPredictions)
        outputdata = {}
        outputdata['songid'] = songtitles[i]
        outputdata['excitedness'] = float(ExcitednessPredictions[i]) / 100
        outputdata['happiness'] = float(HappinessPredictions[i]) / 100
        output.append(outputdata)
    return output
        
