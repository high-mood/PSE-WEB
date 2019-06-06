import requests

from requests.auth import HTTPBasicAuth

from config import SPOTIFY_CLIENT,SPOTIFY_SECRET

def get_user_info(access_token):
    url = "https://api.spotify.com/v1/me"

    headers = {
        'Authorization': "Bearer {}".format(access_token)
    }

    refresh_response = requests.get(url,
                                    headers=headers,
                                    )

    return refresh_response.json()


def get_access_token(refresh_token):
    url = "https://accounts.spotify.com/api/token"



    body = {"grant_type":"refresh_token",
            "refresh_token":refresh_token}

    response =  requests.post(url,data=body,auth=HTTPBasicAuth(SPOTIFY_CLIENT, SPOTIFY_SECRET))
    return response.content

"""
{"access_token":"....",
"token_type":"Bearer",
"expires_in":3600,
"scope":"user-library-read user-library-modify ...."}
"""


