from flask_restplus import Namespace, Resource, fields
from app.utils.tasks import find_song_recommendations
from app.utils import influx, models
from app import app

import dateparser
import datetime

api = Namespace('songs', description='Song information', path="/songs")

user_data = api.model("inserted_data", {
    "songid": fields.String,
    "excitedness": fields.Float,
    "happiness": fields.Float

})


@api.route('/feedback/')
class Song(Resource):
    """Add feedback for song"""

    @api.expect(user_data)
    def post(self):
        """SOmething something add"""
        print(api.payload)
        songid = api.payload['songid']
        excitedness = api.payload['excitedness']
        happy = api.payload['happiness']
        models.Songmood.update_response_mood(songid, excitedness, happy)
