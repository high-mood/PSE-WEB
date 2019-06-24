import json

import requests
from flask_restplus import Namespace, Resource, fields

from app.utils import spotify
from app.utils.models import User

api = Namespace('playlist', description='playlist', path="/playlist")

playlists = api.model('Playlist details', {
    'userid': fields.String,
    'playlists': fields.Nested(api.model('playlist',
                                         {"name": fields.String,
                                          "id": fields.String,
                                          'href': fields.String,
                                          'public': fields.Boolean,
                                          'track_href': fields.String,
                                          'track_count': fields.Integer, }

                                         ))
})


@api.route('/<string:userid>/list/')
class PlaylistList(Resource):
    """Obtain a list of the user's playlist"""

    @api.marshal_with(playlists, envelope='resource')
    def get(self, userid):
        """Get playlist """
        playlists = spotify.get_playlists(userid)
        return {
            'userid': userid,
            'playlists': playlists
        }
