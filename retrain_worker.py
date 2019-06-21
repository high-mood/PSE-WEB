import numpy as np
from sklearn.ensemble import GradientBoostingRegressor as GBR
from joblib import dump, load
from app.utils.tasks import link_features_mood

def main():
    """Retrain the ML model on new data in the database, generated through user-feedback"""
    features = ["response_excitedness", "response_happiness", "mode", "time_signature", "acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "valence", "tempo"]
    data = link_features_mood(get_responses=True)
    trainset = []
    print("test")
    print("Number of songs:" + str(len(data)))
    for song in data:
        print(data)
        row = [song[feature] for feature in features]
        trainset.append(row)
    trainset = np.array(trainset).astype(float)
    energy = [elem[1] for elem in trainset]
    happiness = [elem[2] for elem in trainset]
    traindata = [elem[5:] for elem in trainset]
    E_est = GBR(n_estimators=50, max_depth=3)
    E_est.fit(traindata, energy)
    H_est = GBR(n_estimators=50, max_depth=3)
    H_est.fit(traindata, happiness)
    dump(E_est, 'Retrained-Energy.joblib')
    dump(H_est, 'Retrained-Happiness.joblib')        


if __name__ == "__main__":
    main()
