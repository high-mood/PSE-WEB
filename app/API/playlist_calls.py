import json

import requests
from flask_restplus import Namespace, Resource, fields

from app.utils import spotify
from app.utils.models import User

api = Namespace('playlist', description='playlist', path="/playlist")

user_data = api.model("inserted_data", {
    "songid": fields.String,
    "excitedness": fields.Float,
    "happiness": fields.Float
})






@api.route('/<string:userid>/list/')
class PlaylistList(Resource):
    """Obtain a list of the user's playlist"""

    def get(self, userid):
        """Get playlist """
        userid=  "19h53h2hpk5o4ilshlunb1j9g"
        playlists = spotify.get_playlists(userid)

