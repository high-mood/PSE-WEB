from flask_restplus import Namespace, Resource, fields
from app.utils import influx, models
from app import app

import dateparser
import datetime

api = Namespace('metric', description='Metric over time', path="/metric")

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

possible_metrics = ['acousticness', 'danceability', 'duration_ms', 'energy',
                    'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
                    'speechiness', 'tempo', 'valence']


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


@api.route('/<string:userid>/<string:metric>/<string:start>/<string:end>')
@api.response(400, 'Invalid metric')
@api.response(404, 'No metrics found')
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
            api.abort(400, msg=f"invalid metric")

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
            api.abort(404, msg=f"No metrics found for '{userid}'")


@api.route('/<string:userid>/<string:count>')
class TopGenres(Resource):
    @api.marshal_with(top_genres, envelope='resource')
    def get(self, userid, count):
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc')
        if not recent_songs:
            print('no history found')
            return
        recent_song_list = list(recent_songs.get_points(measurement=userid))
        songids = list(set([song['songid'] for song in recent_song_list]))
        # TODO you can't do this here
        # Artist.query(genres).filter()