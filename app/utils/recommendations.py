from app.utils.models import User
from app.utils.tasks import get_features_moods
from app.utils import spotify

from scipy.spatial import distance
import statistics


def order_songs(songs, target, n):
    """
    It orders songs based on Euclidean distance of the target and recommended songs mood
    :param songs: list of dicts formatted as:
        [{'songid': actual song id, excitedness: actual excitedness, happiness: actual happiness}].
    :param target: the target mood formatted as: (excitedness, happiness).
    :param n: the amount of recommendations that are returned.
    :return: ascending list of n dictionaries formatted as: [{'songid': actual song id, excitedness: actual excitedness,
        happiness: actual happiness}].
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


def calculate_target_mood(target, current):
    """
    Updates the target mood, the new mood is the mean between the target and current.
    :param target: the target mood formatted as: (excitedness, happiness).
    :param current: the current mood formatted as: (excitedness, happiness).
    :return: new target formatted as: (excitedness, happiness).
    """
    return statistics.mean([target[0], current[0]]), statistics.mean([target[1], current[1]])


def recommend_input(tracks, userid, target=(0.0, 0.0), n=5):
    """
    Find recommendations given max 5 song ID's.
    The recommendations are based on the given songs and the given target mood.
    :param tracks: list of given songs.
    :param userid: Spotify user id of the user.
    :param target: the target mood formatted as: (excitedness, happiness).
    :param n: the amount of recommendations that are returned, standard is 5.
    :return: ascending list of n dictionaries formatted as:
        [{'songid': actual song id, excitedness: actual excitedness, happiness: actual happiness}].
    """
    access_token = spotify.get_access_token(User.get_refresh_token(userid))
    return find_song_recommendations(access_token, tracks, target, n, _get_parameter_string())


def recommend_metric(tracks, userid, metric, excitedness, happiness, n=5):
    """
    Find recommendations based on the last 5 songs, the given metric and the current mood.
    :param tracks: list of given songs.
    :param userid: Spotify user id of the user.
    :param metric: keywords for moods and events, the possible keywords are: sad, mellow, angry, excited, dance, study,
        karaoke, neutral.
    :param excitedness: the excitedness of a user.
    :param happiness: the happiness of a user.
    :param n: the amount of recommendations that are returned, standard is 5.
    :return: ascending list of n dictionaries formatted as: [{'songid': actual song id, excitedness: actual excitedness,
        happiness: actual happiness}].
    """
    moods = {'sad': (-10, -10), 'mellow': (-10, 10), 'angry': (10, -10), 'excited': (10, 10), }
    events = {'dance': _get_parameter_string(min_danceablility=0.4,
                                             min_energy=0.5, min_loudness=-10, min_speechiness=0.0,
                                             min_tempo=60, max_acousticness=0.2,
                                             max_instrumentalness=0.15, max_loudness=-2, max_speechiness=0.3,
                                             max_tempo=130),
              'study': _get_parameter_string(min_acousticness=0.6,
                                             min_instrumentalness=0.5, min_loudness=-30,
                                             max_danceablility=0.1, max_energy=0.35, max_instrumentalness=1.0,
                                             max_loudness=-10, max_speechiness=0.1),
              'karaoke': _get_parameter_string(min_energy=0.1,
                                               min_loudness=-15, max_instrumentalness=0.15,
                                               max_loudness=-4, max_speechiness=0.2),
              'neutral': _get_parameter_string()}

    access_token = spotify.get_access_token(User.get_refresh_token(userid))

    # Calculates the target mood and recommends songs based on this target.
    if metric in moods:
        target = calculate_target_mood(moods[metric], (excitedness, happiness))
        return find_song_recommendations(access_token, tracks, target, n, _get_parameter_string())

    # Recommends songs based on parameters corresponding to events, the target mood is the current mood.
    if metric in events:
        return find_song_recommendations(access_token, tracks, (excitedness, happiness), n, events[metric])


def find_song_recommendations(access_token, tracks, target, n, params):
    """
    Find recommendations based on the last 5 songs, the given metric and the current mood.
    :param access_token: A valid access token from the Spotify Accounts service.
    :param tracks: list of given songs.
    :param target: the target mood formatted as: (excitedness, happiness).
    :param n: the amount of recommendations that are returned, standard is 5.
    :param params: Audio feature parameters.
    :return: ascending list of n dictionaries formatted as:
        [{'songid': actual song id, excitedness: actual excitedness, happiness: actual happiness}].
    """
    track_string = '%2C'.join(tracks[:5])
    response = spotify.get_recommendations(access_token, 50, track_string, params)

    song_recommendation = response['tracks']
    recommendations = {song['id']: {'name': song['name']} for song in song_recommendation}

    moods = get_features_moods(recommendations)
    return order_songs(moods, target, n)