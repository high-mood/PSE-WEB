"""
    update_tracks_workers.py
    ~~~~~~~~~~~~
    This file can be utilized as a worker to update the tracks of all users present within the application's database.

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

import requests

from app.utils.models import User
from app.utils.spotify import get_access_token, StatusCodeError
from app.utils.tasks import update_user_tracks

if __name__ == '__main__':
    # We Limit the traceback to keep the log files clear.
    sys.tracebacklimit = 0

    # Update user tracks
    refresh_tokens = User.get_all_tokes()
    for refresh_token in refresh_tokens:
        try:
            access_token = get_access_token(refresh_token)
            update_user_tracks(access_token)
        except requests.exceptions.RequestException as e:
            print(f"RequestsException: {e}", file=sys.stderr)
        except StatusCodeError as e:
            print(f"StatusCodeError: {e}", file=sys.stderr)
