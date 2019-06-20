from flask_restplus import Namespace, Resource, fields
from app.utils.tasks import recommend_input, recommend_metric
from app.utils import influx, models
from app import app, db

import dateparser
import datetime

api = Namespace('tracks', description='Information about tracks (over time)', path="/tracks")


def get_history(userid, song_count, return_songids=False, calc_mood=True):
    """Get the latest song_count tracks for userid."""
    querycount = 3 * song_count
    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])

    if song_count == 0:
        recent_songs = client.query(f'select songid from "{userid}" order by time desc')
    else:
        recent_songs = client.query(f'select songid from "{userid}" order by time desc limit {querycount}')

    if recent_songs:
        history = []
        recent_song_list = list(recent_songs.get_points(measurement=userid))
        songids = list(set([song['songid'] for song in recent_song_list]))
        songids = songids[:song_count] if song_count > 0 else songids
        songmoods = models.Songmood.get_moods(songids)
        excitedness = 0
        happiness = 0
        count = 1

        for songmood in songmoods:
            if calc_mood and songmood.excitedness and songmood.happiness:
                excitedness += songmood.excitedness
                happiness += songmood.happiness
                count += 1 if count != 1 else 0
            print(songids)
            if not return_songids:
                print(songmood)
                song = {}
                song['songid'] = songmood.songid
                song['excitedness'] = songmood.excitedness
                song['happiness'] = songmood.happiness
                song['time'] = [song['time'] for song in recent_song_list][0]
                song['name'] = models.Song.get_song_name(song['songid'])
                history.append(song)

        if calc_mood:
            excitedness /= count
            happiness /= count

        if return_songids:
            return excitedness, happiness, songids
        return excitedness, happiness, history
    return None, None, None


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


@api.route('/history/<string:userid>/<int:song_count>')
@api.response(404, 'No history found')
class History(Resource):
    @api.marshal_with(history, envelope='resource')
    def get(self, userid, song_count):
        """
        Obtain N most recently played songs along with their mood.
        """
        excitedness, happiness, history = get_history(userid, song_count)
        if history:
            return {
                'userid': userid,
                'mean_excitedness': excitedness,
                'mean_happiness': happiness,
                'songs': history
            }
        else:
            api.abort(404, message=f"No history not found for '{userid}'")


possible_metrics = ['acousticness', 'danceability', 'duration_ms', 'energy',
                    'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
                    'speechiness', 'tempo', 'valence']


def parse_time(start, end):
    if start in ('beginning of time' or 'the beginning of time'):
        start = "0"

    start_date = dateparser.parse(start)
    if not start_date:
        api.abort(400, message=f"could not parse '{start}' as start date")

    end_date = dateparser.parse(end)
    if not end_date:
        api.abort(400, message=f"could not parse '{end}' as end date")

    return f"'{start_date.isoformat()}Z'", f"'{end_date.isoformat()}Z'"


metrics = api.model('Metric over time', {
    'userid': fields.String,
    'metric_over_time': fields.Nested(api.model('metric', {
        'time': fields.String,
        'songid': fields.String,
        'acousticness': fields.Float,
        'danceability': fields.Float,
        'duration_ms': fields.Float,
        'energy': fields.Float,
        'instrumentalness': fields.Float,
        'key': fields.Float,
        'liveness': fields.Float,
        'loudness': fields.Float,
        'mode': fields.Float,
        'speechiness': fields.Float,
        'tempo': fields.Float,
        'valence': fields.Float
    }))
})


@api.route('/metrics/<string:userid>/<string:metrics>/<string:song_count>')
@api.response(400, 'Invalid metric')
@api.response(404, 'No metrics found')
class Metric(Resource):
    @api.marshal_with(metrics, envelope='resource')
    def get(self, userid, metrics, song_count=50, start="'1678-09-21T00:20:43.145224194Z'",
            end=str("'" + datetime.datetime.now().isoformat() + "Z'")):
        """
        Obtain metrics of a user within a given timeframe.
        Possible metrics:
        'acousticness', 'danceability', 'duration_ms', 'energy',
        'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
        'speechiness', 'tempo', 'valence'
        """
        metrics = metrics.split(',')
        _, _, songids = get_history(userid, 0)

        if songids:
            songs = db.session.query(models.Song).filter(models.Song.songid.in_((songids)))
            songs_features = []
            for song in songs:
                song.__dict__['time'] = song.__dict__['time_signature']
                features = song.__dict__
                songs_features.append(features)
            return {
                'userid': userid,
                'metric_over_time': songs_features
            }
        else:
            api.abort(404, message=f"No metrics found for '{userid}'")


top_genres = api.model('Top x genres', {
    'userid': fields.String,
    'songs': fields.Nested(api.model('topsongs', {
        'songid': fields.String,
        'name': fields.String,
        'count': fields.Integer
    }))
})


@api.route('/topsongs/<string:userid>/<string:count>')
class TopSongs(Resource):
    @api.marshal_with(top_genres, envelope='resource')
    def get(self, userid, count):
        """Get the top N genres of the user."""
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc')
        if not recent_songs:
            print('no history found')
            return {
                'userid': userid,
                'songs': []
            }
        recent_song_list = list(recent_songs.get_points(measurement=userid))
        songids = [song['songid'] for song in recent_song_list]
        songdata = db.session.query(models.Song).filter(models.Song.songid.in_((songids))).all()
        songs = {song.songid: song.name for song in songdata}
        counted_songs = sorted([(songs[id], id, songids.count(id)) for id in list(set(songids))], key=lambda val: val[2], reverse=True)
        top_x = counted_songs[:int(count)]
        return_data = [{'songid': data[1], 'name': data[0], 'count':data[2]} for data in top_x]
        return {
            'userid': userid,
            'songs': return_data
        }


recommendations = api.model('Song recommendations', {
    'userid': fields.String,
    'recommendations': fields.Nested(api.model('recommendation', {
        'songid': fields.String,
        'excitedness': fields.Float,
        'happiness': fields.Float
    }))
})


@api.route('/recommendation/<string:userid>/<string:songid>/<float:excitedness>/<float:happiness>')
@api.response(404, 'No recommendations found')
class Recommendation_song(Resource):
    @api.marshal_with(recommendations, envelope='resource')
    def get(self, userid, songid, excitedness, happiness):
        """
        Obtain recommendations based on a song along with its excitedness and happiness.
        """
        recs = recommend_input([songid], userid, target=(float(excitedness), float(happiness)))

        if recs:
            return {
                'userid': userid,
                'recommendations': recs
            }
        else:
            api.abort(404, message=f"No recommendations not found for '{userid}'")


@api.route('/recommendation/<string:userid>/<string:metric>')
@api.response(404, 'No recommendations found')
class Recommendation_metric(Resource):
    @api.marshal_with(recommendations, envelope='resource')
    def get(self, userid, metric):
        """
        Obtain recommendations based on an metric selected by user.
        """
        excitedness, happiness, songids = get_history(userid, 0, songids=True)
        recs = recommend_metric(songids[:6], userid, metric, excitedness, happiness)

        if recs:
            return {
                'userid': userid,
                'recommendations': recs
            }
        else:
            api.abort(404, message=f"No recommendations not found for '{userid}'")
