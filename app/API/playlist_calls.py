"""
    playlist_calls.py
    ~~~~~~~~~~~~
    The functionality within this file contains the API calls...

    TODO

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

from flask_restplus import Namespace, Resource, fields

from app.utils import spotify

api = Namespace('playlist', description='playlist', path="/playlist")


@api.route('/<string:userid>/list/')
class PlaylistList(Resource):
    """Obtain a list of the user's playlist"""

    # Output format
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

    @api.marshal_with(playlists, envelope='resource')
    def get(self, userid):
        """Get playlist """
        # TODO You should just call the spotify api!
        api.abort(403, message=f"Just call the Spotify API")
        playlists = spotify.get_playlists(userid)
        return {
            'userid': userid,
            'playlists': playlists
        }
