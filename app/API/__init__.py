"""
    API
    __init__.py
    ~~~~~~~~~~~~
    This file contains the initialization code for the API.

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

from flask_restplus import Api
from flask import Blueprint
from app import app

from .user_calls import api as user_name_space
from .track_calls import api as track_name_space
from .playlist_calls import api as playlist_name_space

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)

api.add_namespace(user_name_space)
api.add_namespace(track_name_space)
api.add_namespace(playlist_name_space)
