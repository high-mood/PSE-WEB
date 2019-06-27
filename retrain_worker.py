"""
    retrain_worker.py
    ~~~~~~~~~~~~
    This file implements functionality to retrain the machine learning model's used in the predictions of mood.
    These predictions are altered based upon user supplied feedback.

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

import numpy as np
from joblib import dump
from sklearn.ensemble import GradientBoostingRegressor as GBR

from app.utils.tasks import link_features_mood


def main():
    """Retrain the ML model on new data in the database, generated through user-feedback"""
    features = ["response_excitedness", "response_happiness", "mode", "time_signature", "acousticness",
                "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "valence", "tempo"]
    data = link_features_mood(get_responses=True)
    train_set = []
    print("test")
    print("Number of songs:" + str(len(data)))
    for song in data:
        print(data)
        row = [song[feature] for feature in features]
        train_set.append(row)
    train_set = np.array(train_set).astype(float)
    energy = [elem[1] for elem in train_set]
    happiness = [elem[2] for elem in train_set]
    train_data = [elem[5:] for elem in train_set]
    excited_est = GBR(n_estimators=50, max_depth=3)
    excited_est.fit(train_data, energy)
    happy_est = GBR(n_estimators=50, max_depth=3)
    happy_est.fit(train_data, happiness)
    dump(excited_est, 'Retrained-Energy.joblib')
    dump(happy_est, 'Retrained-Happiness.joblib')


if __name__ == "__main__":
    main()
