"""
    update_moods_workers.py
    ~~~~~~~~~~~~
    This file can be utilized as a worker to update the moods of all users present within the application's database.

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

from app.utils.models import User
from app.utils.tasks import get_last_n_minutes


def main():
    duration = sys.argv[1]
    # We Limit the traceback to keep the log files clear.
    sys.tracebacklimit = 0
    userids = User.get_all_userids()

    for userid in userids:
        get_last_n_minutes(duration, userid)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main()
    else:
        print('Add duration to generate mean mood for: run.py <duration (i.e. 1h, 1d, 1w etc)>')
