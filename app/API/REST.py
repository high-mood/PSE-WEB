# TODO: restructur this code
# TODO: unit tests

from . import views
from app import app
from flask_restplus import Api, Resource, fields
from .exceptions import NoResultsFound, InvalidValue
from flask import Blueprint, jsonify
from app import models
from . import influx

import numpy as np
import dateparser
import datetime


possible_metrics = ['acousticness', 'danceability', 'duration_ms', 'energy',
                    'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
                    'speechiness', 'tempo', 'valence']


def parse_time(start, end):
    if start in ('beginning of time' or 'the beginning of time'):
        start = "0"

    start_date = dateparser.parse(start)
    if not start_date:
        raise InvalidValue(f"could not parse '{start}' as start date")

    end_date = dateparser.parse(end)
    if not end_date:
        raise InvalidValue(f"could not parse '{end}' as end date")

    return f"'{start_date.isoformat()}Z'", f"'{end_date.isoformat()}Z'"


blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)

user_name_space = api.namespace('user', description='User information', path="/user")
mood_name_space = api.namespace('mood', description='Mood over time', path="/mood")
metric_name_space = api.namespace('metric', description='Metric over time', path="/metric")
history_name_space = api.namespace('history', description='Song history', path="/history")

@api.errorhandler
def default_error_handler(error):
    """ Default error handler. """
    if not app.config['DEBUG']:
        return {'message': 'An unhandled exception occurred.'}, getattr(error, 'code', 500)


@api.errorhandler(InvalidValue)
@api.errorhandler(NoResultsFound)
def error_handler(error):
    return {'message': str(error)}, 404


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


@user_name_space.route("/<string:userid>")
class User(Resource):
    @api.marshal_with(user_info, envelope='resource')
    def get(self, userid):
        """
        Obtain all of a user's account information.
        """

        user = models.User.query.filter_by(userid=userid).first()
        if not user:
            raise NoResultsFound("userid not found")

        return user


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


@mood_name_space.route('/<string:userid>/<string:start>/<string:end>')
class Mood(Resource):
    @api.marshal_with(moods, envelope='resource')
    def get(self, userid, start="'1678-09-21T00:20:43.145224194Z'",
            end=str("'" + datetime.datetime.now().isoformat() + "Z'")):
        """
        Obtain moods of a user within a given time frame.
        """
        start, end = parse_time(start, end)
        print(start, end)

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
            raise NoResultsFound(f"No moods found for '{userid}'")


metrics = api.model('Metric over time', {
    'userid': fields.String,
    'metric_over_time': fields.Nested(api.model('metric', {
            'time': fields.String,
            'value': fields.Float,
        }))
    })


@metric_name_space.route('/<string:userid>/<string:metric>/<string:start>/<string:end>')
class Metric(Resource):
    @api.marshal_with(metrics, envelope='resource')
    def get(self, userid, metric, start="'1678-09-21T00:20:43.145224194Z'",
            end=str("'" + datetime.datetime.now().isoformat() + "Z'")):
        """
        Obtain metric of a user within a given timeframe.
        Possible metrics:
        'acousticness', 'danceability', 'duration_ms', 'energy',
        'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
        'speechiness', 'tempo', 'valence'
        """
        if metric not in possible_metrics:
            raise InvalidValue("invalid metric")

        start, end = parse_time(start, end)

        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        user_metrics = client.query(f'select {metric} from "{userid}" where time > {start} and time < {end}')

        if user_metrics:
            metric_list = list(user_metrics.get_points(measurement=userid))
            for timed_metric in metric_list:
                timed_metric['value'] = timed_metric.pop('tempo')

            return {
                'userid': userid,
                'metric_over_time': metric_list
            }
        else:
            raise NoResultsFound(f"No metrics not found for '{userid}'")


history = api.model('Song history with mood', {
    'userid': fields.String,
    'mean_excitedness': fields.Float,
    'mean_happiness': fields.Float,
    'songs': fields.Nested(api.model('song', {
            'name': fields.String,
            'exitedness': fields.Float,
            'happiness': fields.Float
        }))
    })


@metric_name_space.route('/<string:userid>/<integer:songcount')
class Metric(Resource):
    @api.marshal_with(history, envelope='resource')
    def get(self, userid, songcount):
        """
        Obtain N most recently played songs along with their mood.
        """
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc limit {songcount}')

        if recent_songs:
            recent_songs = list(user_metrics.get_points(measurement=userid))
            print(recent_songs)

            return {
                'userid': userid,
                'songs': recent_songs
            }
        else:
            raise NoResultsFound(f"No metrics not found for '{userid}'")
