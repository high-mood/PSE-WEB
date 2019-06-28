import os

from flask import Flask
from flask_cors import CORS
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
app.secret_key = os.environ.get("APP_SECRET", config.SECRET)
db = SQLAlchemy(app)

oauth = OAuth()
spotifysso = oauth.remote_app('spotify',
                              base_url='https://accounts.spotify.com',
                              access_token_url='https://accounts.spotify.com/api/token',
                              authorize_url='https://accounts.spotify.com/authorize',
                              consumer_key=app.config['SPOTIFY_CLIENT'],
                              consumer_secret=app.config['SPOTIFY_SECRET'],
                              request_token_params={'scope': ('user-read-recently-played,'
                                                              'user-library-modify,'
                                                              'user-read-email',
                                                              'playlist-modify-public',
                                                              'playlist-modify-private',
                                                              'user-library-read',
                                                              'user-read-birthdate',
                                                              'user-read-private',
                                                              'user-read-currently-playing'
                                                              )
                                                    },
                              request_token_url=None
                              )
oauth.init_app(app)

from app import views
from app import API
