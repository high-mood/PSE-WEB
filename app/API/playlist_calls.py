from flask_restplus import Namespace, Resource, fields

api = Namespace('playlist', description='playlist', path="/playlist")

user_data = api.model("inserted_data", {
    "songid": fields.String,
    "excitedness": fields.Float,
    "happiness": fields.Float
})


@api.route('/list/')
class PlaylistList(Resource):
    """Add feedback for song"""

    def get(self, userid):
        pass
