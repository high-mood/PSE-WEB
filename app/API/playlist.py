from flask_restplus import Namespace, Resource, fields
from app.utils.tasks import find_song_recommendations
from app.utils import influx, models
from app import app

import dateparser
import datetime

api = Namespace('playlist', description='playlist', path="/playlist")

user_data = api.model("inserted_data", {
    "songid": fields.String,
    "excitedness": fields.Float,
    "happiness": fields.Float

})


@api.route('/list/')
class Song(Resource):
    """Add feedback for song"""

    def get(self,userid):
        pass