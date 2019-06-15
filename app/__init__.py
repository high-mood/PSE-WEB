import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.environ.get("APP_SECRET", config.SECRET)  # THIS SHOULD BE SOMETHING RANDOM
db = SQLAlchemy(app)

# TODO: Make this dynamic, allow user to select scopes
oauth = OAuth()
spotifysso = oauth.remote_app('spotify',
                              base_url='https://accounts.spotify.com',
                              access_token_url='https://accounts.spotify.com/api/token',
                              authorize_url='https://accounts.spotify.com/authorize',
                              consumer_key=config.SPOTIFY_CLIENT,
                              consumer_secret=config.SPOTIFY_SECRET,
                              request_token_params={'scope': ('user-read-recently-played,'
                                                              'user-library-modify,'
                                                              'user-read-email',
                                                              'playlist-modify-public',
                                                              'playlist-modify-private',
                                                              'user-library-read',
                                                              'user-read-birthdate',
                                                              'user-read-private',
                                                              # 'user-top-read',
                                                              # TODO: https://github.com/spotify/web-api/issues/1262
                                                              'user-read-currently-playing'
                                                              )

                                                    },
                              request_token_url=None
                              )
oauth.init_app(app)

from app import views
from app import API

