from flask_restplus import Namespace, Resource, fields
from app.utils import influx, models
from app import app

import dateparser
import datetime

api = Namespace('user', description='Information about user (over time)', path="/user")

user_info = api.model('UserInfo', {
    'userid': fields.String,
    'email': fields.String,
    'display_name': fields.String,
    'image_url': fields.String,
    'birthdate': fields.DateTime,
    'country': fields.String,
    'is_premium': fields.Boolean,
    'refresh_token': fields.String,
    'user_is_active': fields.Boolean
})


@api.route('/info/<string:userid>')
@api.response(404, 'Userid not found')
class User(Resource):
    @api.marshal_with(user_info, envelope='resource')
    def get(self, userid):
        """
        Obtain all of a user's account information.
        """
        user = models.User.get_user(userid)
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


@api.route('/mood/<string:userid>/<int:start>/<int:end>')
@api.response(400, 'Invalid date')
@api.response(404, 'No moods found')
class Mood(Resource):
    @api.marshal_with(moods, envelope='resource')
    # ALL ZERO PADDED TODO DOCUMENT
    def get(self=None, userid="snipy12", start=3, end=24, endoftime=False):
        """
        Obtain moods of a user within a given time frame in hours of a day.
        """

        if start > end:
            api.abort(400, msg="Timeframe incorrect: start > end")

        if start > 23 or start < 0:
            api.abort(400, msg="Timeframe incorrect: start time not between 0 - 23")

        if end > 24 or end < 1:
            api.abort(400, msg="Timeframe incorrect: end time not between 1 - 24")

        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        user_mood = influx.get_mood(client, userid)

        if user_mood:
            resultset = []
            excitedness = 0
            happiness = 0
            total_songs = 0
            for record in user_mood[userid]:
                mood_time = record['time'].split(".")[0]
                mood_time = datetime.datetime.strptime(mood_time[:-1], '%Y-%m-%dT%H:%M:%S')
                mood_hour = mood_time.hour

                if start <= mood_hour <= end:
                    total_songs += record['songcount']
                    excitedness += record['excitedness'] * record['songcount']
                    happiness += record['happiness'] * record['songcount']
                    resultset.append(record)
            if total_songs < 1:
                api.abort(404, msg=f"No moods found for '{userid}'")

            return {
                'userid': userid,
                'mean_excitedness': excitedness / total_songs,
                'mean_happiness': happiness / total_songs,
                'sum_song_count': total_songs,
                'moods': resultset
            }
        else:
            api.abort(404, msg=f"No moods found for '{userid}'")
