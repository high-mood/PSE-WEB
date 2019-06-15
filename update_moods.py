from app.tasks import get_last_n_minutes
from app.models import User
import sys


def main():
    duration = sys.argv[1]
    sys.tracebacklimit = 0
    userids = User.get_all_users()

    for userid in userids:
        get_last_n_minutes(duration, userid)


if __name__ == '__main__':
    # We Limit the traceback to keep the log files clear.
    if len(sys.argv) == 2:
        main()
    else:
        print('Add duration to generate mean mood for: run.py <duration (i.e. 1h, 1d, 1w etc)>')
