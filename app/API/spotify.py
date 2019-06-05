import requests
import ast


def get_user_info(access_token):
    url = "https://api.spotify.com/v1/me"

    headers = {
        'Authorization': "Bearer {}".format(access_token)
    }

    refresh_response = requests.get(url,
                                    headers=headers,
                                    )

    return refresh_response.json()
