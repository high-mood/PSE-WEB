"""
    exceptions.py
    ~~~~~~~~~~~~
    This file contains custom exceptions to handle invalid input.

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

class StatusCodeError(Exception):
    """
    There was an request that did not return an 200 status code.

    Expects body to be formatted as described in:
    https://developer.spotify.com/documentation/web-api/#response-schema
    """

    def __init__(self, response):
        if response.status_code == 204:
            super().__init__("204 NO CONTENT")
            return
        if response.status_code == 429:
            super().__init__(f"Timeout for {response.headers['Retry-After']} seconds")
            return

        body = response.json()
        # Spotify authentication Error
        if 'error' and 'error_description' in body['error']:
            super().__init__(f"Error {body['error']['error']}: {body['error']['error_description']}")
        # Regular spotify Error
        elif 'status' and 'message' in body['error']:
            super().__init__(f"Status {body['error']['status']}: {body['error']['message']}")
