from app.API.spotify import get_access_token
from app.tasks import update_user_tracks
from app.models import Songmood
import sys

if __name__ == '__main__':
    # We Limit the traceback to keep the log files clear.
    sys.tracebacklimit = 0
    refresh_tokens = Songmood.get_all_tokes()
    for refresh_token in refresh_tokens:
        access_token = get_access_token(refresh_token)
        update_user_tracks(access_token)
