from flask_restplus import Namespace, Resource, fields
from app.utils import influx, models
from app import app
from app.utils.tasks import find_song_recommendations

import dateparser
import datetime

api = Namespace('tracks', description='Information about tracks of a user', path="/tracks")
# api = Namespace('recommendation', description='Song recommendations', path="/recommendation")
# api = Namespace('metric', description='Metric over time', path="/metric")

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


@api.route('/<string:userid>/<int:songcount>')
@api.response(404, 'No history found')
class History(Resource):
    @api.marshal_with(history, envelope='resource')
    def get(self, userid, songcount):
        """
        Obtain N most recently played songs along with their mood.
        """
        querycount = 3 * songcount
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc limit {querycount}')
        if recent_songs:
            history = []
            recent_song_list = list(recent_songs.get_points(measurement=userid))
            songids = list(set([song['songid'] for song in recent_song_list]))
            songids = songids[:songcount] if songcount > 0 else songids
            songmoods = models.Songmood.get_moods(songids)
            excitedness = 0
            happiness = 0
            mean_count = 1

            for songmood in songmoods:
                if songmood.excitedness and songmood.happiness:
                    excitedness += songmood.excitedness
                    happiness += songmood.happiness
                    mean_count += 1 if mean_count != 1 else 0
                song = {}
                song['songid'] = songmood.songid
                song['excitedness'] = songmood.excitedness
                song['happiness'] = songmood.happiness
                song['time'] = [song['time'] for song in recent_song_list][0]
                song['name'] = models.Song.get_song_name(song['songid'])
                history.append(song)
            excitedness /= mean_count
            happiness /= mean_count

            return {
                'userid': userid,
                'mean_excitedness': excitedness,
                'mean_happiness': happiness,
                'songs': history
            }
        else:
            api.abort(404, msg=f"No history not found for '{userid}'")


metrics = api.model('Metric over time', {
    'userid': fields.String,
    'metric_over_time': fields.Nested(api.model('metric', {
        'time': fields.String,
        'value': fields.Float,
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


top_genres = api.model('Top x genres', {
    'userid': fields.String,
    'genres': fields.Nested(api.model('topgenres', {
        'genre': fields.String,
        'count': fields.Integer
    }))
})


@api.route('/<string:userid>/<string:count>')
class TopGenres(Resource):
    @api.marshal_with(top_genres, envelope='resource')
    def get(self, userid, count):
        """Get the top N genres of the user."""
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc')
        if not recent_songs:
            print('no history found')
            return
        recent_song_list = list(recent_songs.get_points(measurement=userid))
        songids = list(set([song['songid'] for song in recent_song_list]))
        # TODO you can't do this here
        # Artist.query(genres).filter()


recommendations = api.model('Song recommendations', {
    'userid': fields.String,
    'recommendations': fields.Nested(api.model('recommendation', {
        'songid': fields.String,
        'excitedness': fields.String,
        'happiness': fields.List(fields.String)
    }))
})


@api.route('<string:userid>/<int:recommendation_count>')
@api.response(404, 'No recommendations found')
class Recommendation(Resource):
    @api.marshal_with(recommendations, envelope='resource')
    def get(self, userid, recommendation_count):
        """
        Obtain recommendations for the user along with their features.
        """
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc limit 5')
        if recent_songs:
            recent_songs = list(recent_songs.get_points(measurement=userid))
            songids = [song['songid'] for song in recent_songs]
            recs = find_song_recommendations(songids, userid, recommendation_count)
            if recs:
                return {
                    'userid': userid,
                    'recommendations': recs
                }
            else:
                api.abort(404, msg=f"No recommendations not found for '{userid}'")
