"""
    playlist_calls.py
    ~~~~~~~~~~~~
    This file contains the structure of the playlist API with functions to handle basic GET and POST requests.
    In the current version of the website this api is not featured, however the functionality is easily included.


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


@api.route('list/<string:userid>')
class PlaylistList(Resource):
    """
    Obtain a list of the user's playlist
    :param userid: Unique identifier for a user.
    """

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
        """Get a list playlists"""
        playlists = spotify.get_playlists(userid)
        return {
            'userid': userid,
            'playlists': playlists
        }
