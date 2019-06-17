from app.API.spotify import get_access_token, StatusCodeError
from app.tasks import update_user_tracks
from app.models import User
import requests
import sys

if __name__ == '__main__':
    # We Limit the traceback to keep the log files clear.
    # sys.tracebacklimit = 0

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
