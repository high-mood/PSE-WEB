import requests
from requests.auth import HTTPBasicAuth
from config import SPOTIFY_CLIENT, SPOTIFY_SECRET


class StatusCodeError(requests.exceptions.RequestException):
    """An request did not return an 200 status code."""
    pass


def get_artists(access_token, artistids):
    """
    Get Spotify catalog information for several artists based on their Spotify IDs.

    Parameters
    ----------
    access_token : string
        A valid access token from the Spotify Accounts service.
    artistids : array_like
        A list of the Spotify IDs for the artists.
    Returns
    -------
    response : json
        Responce body which contains a list of object whose key is "artists" and
        whose value is an array of artist objects in JSON format.
    """
    url = "https://api.spotify.com/v1/artists?ids={}".format(",".join(artistids))

    return _get_basic_request(access_token, url)


def get_audio_features(access_token, trackids):
    url = "https://api.spotify.com/v1/audio-features/?ids={}".format(",".join(trackids))

    return _get_basic_request(access_token, url)


def get_recently_played(access_token, limit=50):
    url = "https://api.spotify.com/v1/me/player/recently-played?limit={}".format(limit)

    return _get_basic_request(access_token, url)


def get_user_info(access_token):
    url = "https://api.spotify.com/v1/me"

    return _get_basic_request(access_token, url)


def _get_basic_request(access_token, url):
    headers = {'Authorization': "Bearer {}".format(access_token)}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise StatusCodeError(f"Received status code: {response.status_code}")

    return response.json()


def get_access_token(refresh_token):
    url = "https://accounts.spotify.com/api/token"

    body = {"grant_type": "refresh_token",
            "refresh_token": refresh_token}

    response = requests.post(url, data=body, auth=HTTPBasicAuth(SPOTIFY_CLIENT, SPOTIFY_SECRET))

    if response.status_code != 200:
        raise StatusCodeError(f"Received status code: {response.status_code}")

    try:
        access_token = response.json()["access_token"]
    except KeyError:
        raise ValueError("refresh_token was not valid")

    return access_token

# response.content
#   {"access_token":"....",
#    "token_type":"Bearer",
#    "expires_in":3600,
#    "scope":"user-library-read user-library-modify ...."}
