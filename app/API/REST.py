# TODO: restructur this code
# TODO: unit tests

from app.song_recommendations import find_song_recommendations
from .exceptions import NoResultsFound, InvalidValue
from flask_restplus import Api, Resource, fields
from flask import Blueprint, jsonify
from app import models
from app import app
from . import views
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
recommendation_name_space = api.namespace('recommendation', description='Song recommendations', path="/recommendation")

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

top_genres = api.model('Top x genres', {
    'userid': fields.String,
    'genres': fields.Nested(api.model('topgenres', {
        'genre': fields.String,
        'count': fields.Integer
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

# @metric_name_space.route('/<string:userid>/<string:count>')
# class TopGenres(Resource):
#     @api.marshal_with(top_genres, envelope='resource')
#     def get(self, userid, count):


history = api.model('Song history with mood', {
    'userid': fields.String,
    'mean_excitedness': fields.Float,
    'mean_happiness': fields.Float,
    'songs': fields.Nested(api.model('song', {
        'songid': fields.String,
        'name': fields.String,
        'time': fields.String,
        'excitedness': fields.Float,
        'happiness': fields.Float
    }))
})


@history_name_space.route('/<string:userid>/<int:songcount>')
class History(Resource):
    @api.marshal_with(history, envelope='resource')
    def get(self, userid, songcount):
        """
        Obtain N most recently played songs along with their mood.
        """
        querycount = 3 * songcount
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc limit {querycount}')
        # print(recent_songs)
        if recent_songs:
            history = []
            recent_song_list = list(recent_songs.get_points(measurement=userid))
            songids = list(set([song['songid'] for song in recent_song_list]))
            moods = models.Songmood.get_moods(songids)
            e, h = list(zip(*moods))
            excitedness, happiness = [val[0] for val in e], [val[0] for val in h]
            mean_excitedness = np.mean(excitedness)
            mean_happiness = np.mean(happiness)

            for i, songid in enumerate(songids):
                song = {}
                song['songid'] = songid
                song['excitedness'] = excitedness[i]
                song['happiness'] = happiness[i]
                song['time'] = [song['time'] for song in recent_song_list][0]
                song['name'] = models.Song.get_song_name(song['songid'])
                history.append(song)

            return {
                'userid': userid,
                'mean_excitedness': mean_excitedness,
                'mean_happiness': mean_happiness,
                'songs': history
            }
        else:
            raise NoResultsFound(f"No metrics not found for '{userid}'")


recommendationers = api.model('Song recommendations', {
    'userid': fields.String,
    'recommendations': fields.Nested(api.model('recommendation', {
        'songid': fields.String,
        'song_url': fields.String,
        'artists': fields.List(fields.String),
        'name': fields.String,
        'image_url': fields.String
    }))
})


@recommendation_name_space.route('<string:userid>/<int:recommendation_count>')
class Recommendation(Resource):
    @api.marshal_with(recommendationers, envelope='resource')
    def get(self, userid, recommendation_count):
        """
        Obtain {recommendation_count} recommendations for user {userid} along
        with their features.
        """
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc limit 5')
        if recent_songs:
            recent_songs = list(recent_songs.get_points(measurement=userid))
            songids = [song['songid'] for song in recent_songs]
            recs = find_song_recommendations(songids, userid, recommendation_count)
            print(recs)
            if recs:
                return {
                    'userid': userid,
                    'recommendations': recs
                }


features = api.model('Song features', {
    'duration_ms': fields.Float,
    'key': fields.Float,
    'mode': fields.Float,
    'time_signature': fields.Float,
    'acousticness': fields.Float,
    'danceability': fields.Float,
    'energy': fields.Float,
    'instrumentalness': fields.Float,
    'liveness': fields.Float,
    'loudness': fields.Float,
    'speechiness': fields.Float,
    'valence': fields.Float,
    'tempo': fields.Float
})

artist_info = api.model('Artist info', {
    'artistid': fields.String,
    'name': fields.String,
    'popularity': fields.Integer,
    'genres': fields.List(fields.String)
})
