from app.API.spotify import get_access_token
from app.tasks import update_user_tracks, get_last_n_minutes
from app.models import User
import sys

if __name__ == '__main__':
    # We Limit the traceback to keep the log files clear.
    sys.tracebacklimit = 0

    # Update user tracks
    refresh_tokens = User.get_all_tokes()
    for refresh_token in refresh_tokens:
        access_token = get_access_token(refresh_token)
        update_user_tracks(access_token)

    # Update user mood
    userids = User.get_all_users()
    for userid in userids:
        get_last_n_minutes('15m', userid)
