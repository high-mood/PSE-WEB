from flask_restplus import Namespace, Resource, fields
from app.utils import models

api = Namespace('songs', description='Song information', path="/songs")

user_data = api.model("inserted_data", {
    "songid": fields.String,
    "excitedness": fields.Float,
    "happiness": fields.Float
})


@api.route('/mood/<string:userid>')
class SongFeedback(Resource):
    """ Add feedback for song. """

    @api.expect(user_data)
    def post(self):
        """SOmething something add"""
        songid = api.payload['songid']
        excitedness = api.payload['excitedness']
        happy = api.payload['happiness']
        models.Songmood.update_response_mood(songid, excitedness, happy)
