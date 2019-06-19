from flask_restplus import Namespace, Resource, fields
from app.utils import influx, models
from app import app

import numpy as np
import dateparser
import datetime

api = Namespace('user', description='User information', path="/user")

user_info = api.model('UserInfo', {
    'userid': fields.String,
    'email': fields.String,
    'display_name': fields.String,
    'image_url': fields.String,
    'birthdate': fields.DateTime,
    'country': fields.String,
    'is_premium': fields.Boolean,
    'refresh_tokens': fields.String,
    'user_is_active': fields.Boolean
})


@api.route("/<string:userid>")
@api.response(404, 'Userid not found')
class User(Resource):
    @api.marshal_with(user_info, envelope='resource')
    def get(self, userid):
        """
        Obtain all of a user's account information.
        """
        user = models.User.query.filter_by(userid=userid).first()
        if not user:
            api.abort(404, msg="userid not found")

        return user


def parse_time(start, end):
    if start in ('beginning of time' or 'the beginning of time'):
        start = "0"

    start_date = dateparser.parse(start)
    if not start_date:
        api.abort(400, msg=f"could not parse '{start}' as start date")

    end_date = dateparser.parse(end)
    if not end_date:
        api.abort(400, msg=f"could not parse '{end}' as end date")

    return f"'{start_date.isoformat()}Z'", f"'{end_date.isoformat()}Z'"


moods = api.model('Mood over time', {
    'userid': fields.String,
    'mean_excitedness': fields.Float,
    'mean_happiness': fields.Float,
    'sum_song_count': fields.Integer,
    'moods': fields.Nested(api.model('mood', {
        'time': fields.String,
        'excitedness': fields.Float,
        'happiness': fields.Float,
        'songcount': fields.Integer
    }))
})


@api.route('/<string:userid>/<string:start>/<string:end>')
@api.response(400, 'Invalid date')
@api.response(404, 'No moods found')
class Mood(Resource):
    @api.marshal_with(moods, envelope='resource')
    def get(self, userid, start="'1678-09-21T00:20:43.145224194Z'",
            end=str("'" + datetime.datetime.now().isoformat() + "Z'")):
        """
        Obtain moods of a user within a given time frame.
        """
        start, end = parse_time(start, end)

        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        user_mood = client.query(f'select excitedness, happiness, songcount from "{userid}" where time > {start} and time < {end}')

        if user_mood:
            mood_list = list(user_mood.get_points(measurement=userid))

            v = [[mood['excitedness'], mood['happiness'], mood['songcount']] for mood in mood_list]
            mean_happiness, mean_excitedness, _ = np.mean(v, axis=0)
            _, _, sum_song_count = np.sum(v, axis=0)

            return {
                'userid': userid,
                'mean_excitedness': mean_excitedness,
                'mean_happiness': mean_happiness,
                'sum_song_count': sum_song_count,
                'moods': mood_list
            }
        else:
            api.abort(404, msg=f"No moods found for '{userid}'")
