from app.API.spotify import get_access_token
from app.tasks import update_user_tracks
from app.models import User

if __name__ == "__main__":
    refresh_tokens = User.get_all_tokes()
    for refresh_token in refresh_tokens:
        access_token = get_access_token(refresh_token)
        update_user_tracks(access_token)
