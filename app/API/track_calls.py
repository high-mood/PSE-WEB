"""
    track_calls.py
    ~~~~~~~~~~~~
    This file contains the structure of the track API with functions to handle basic GET and POST requests.

    :copyright: 2019 Moodify (High-Mood)
    :authors:
           "Stan van den Broek",
           "Mitchell van den Bulk",
           "Mo Diallo",
           "Arthur van Eeden",
           "Elijah Erven",
           "Henok Ghebrenigus",
           "Jonas van der Ham",
           "Mounir El Kirafi",
           "Esmeralda Knaap",
           "Youri Reijne",
           "Siwa Sardjoemissier",
           "Barry de Vries",
           "Jelle Witsen Elias"
"""

from flask_restplus import Namespace, Resource, fields

from app import app
from app.utils import influx, models
from app.utils.recommendations import recommend_input, recommend_metric

api = Namespace('tracks', description='Information about tracks (over time)', path="/tracks")


def get_history(userid, song_count, return_songids=False, calc_mood=True):
    """
    Get the latest song_count tracks for userid.
    :param userid: Unique identifier for a user.
    :param song_count: How many songs should be returned.
    :return_songids: Return list of songids instead of history with features.
    :param calc_mood: Calculate the average excitedness and happiness.
    :return: Average of happiness and happiness, list of dictionary containing songs.
    """
    client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])

    recent_songs = influx.get_songs(client, userid, song_count)

    if recent_songs:
        history = []
        # Remove duplicates songs
        songids = [song['songid'] for song in recent_songs]
        songids = songids[:song_count] if song_count > 0 else songids
        songmoods = models.Songmood.get_moods(songids)
        excitedness = 0
        happiness = 0
        count = 1

        for i, songmood in enumerate(songmoods):
            if calc_mood and songmood.excitedness and songmood.happiness:
                excitedness += songmood.excitedness
                happiness += songmood.happiness
                count += 1 if count != 1 else 0

            if not return_songids:
                song = {'songid': songmood.songid,
                        'excitedness': songmood.excitedness,
                        'happiness': songmood.happiness,
                        'time': recent_songs[i]['time'],
                        'name': models.Song.get_song_name(songmood.songid)}
                history.append(song)

        if calc_mood:
            excitedness /= count
            happiness /= count

        if return_songids:
            return excitedness, happiness, songids

        return excitedness, happiness, history

    return None, None, None


@api.route('/mood')
class SongFeedback(Resource):
    """
    Receive mood response for a given song and update this in SQL.
    """

    # Output format
    user_data = api.model("inserted_data", {
        "songid": fields.String,
        "excitedness": fields.Float,
        "happiness": fields.Float
    })

    @api.expect(user_data)
    def post(self):
        """Update a mood response in the database"""
        songid = api.payload['songid']
        excitedness = api.payload['excitedness']
        happy = api.payload['happiness']
        models.Songmood.update_response_mood(songid, excitedness, happy)


# Output format for history and topsongs.
@api.route('/history/<string:userid>/<int:song_count>')
@api.response(404, 'No history found')
class History(Resource):
    """
    Return the last song_count songs of the user.
    :param userid: Unique identifier for a user.
    :param song_count: Specifies how many songs of the history to return.
    """

    # Output format
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

    @api.marshal_with(history, envelope='resource')
    def get(self, userid, song_count):
        """
        Obtain song_count most recently played songs along with their mood.
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


@api.route('/topsongs/<string:userid>/<string:song_count>')
class TopSongs(Resource):
    """
    Return the top songs of a user by counting the number of listens.
    :param userid: Unique identifier for a user
    :param song_count: Specifies how many songs of the history to return
    """
    # Output format
    top_songs = api.model('Song history with mood', {
        'userid': fields.String,
        'songs': fields.Nested(api.model('song', {
            'songid': fields.String,
            'name': fields.String,
            'excitedness': fields.Float,
            'happiness': fields.Float
        }))
    })

    @api.marshal_with(top_songs, envelope='resource')
    def get(self, userid, song_count):
        """Get the top N genres of the user."""
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])

        recent_songs = influx.get_songs(client, userid)

        if not recent_songs:
            api.abort(404, message=f"No history found for '{userid}'")

        songids = [song['songid'] for song in recent_songs]
        result = models.Song.get_songs_with_mood(songids)
        counted_songs = sorted([((song, songmood), songids.count(song.songid)) for song, songmood in result],
                               key=lambda val: val[1], reverse=True)
        top_x = counted_songs[:int(song_count)]

        return {
            'userid': userid,
            'songs': [{**song.__dict__, **songmood.__dict__} for (song, songmood), count in top_x]
        }


@api.route('/metrics/<string:userid>/<int:song_count>')
@api.response(400, 'Invalid metric')
@api.response(404, 'No metrics found')
class Metric(Resource):
    """
    Return a historical list of songs for a user with features and moods.
    :param userid: Unique identifier for a user.
    :param song_count: Specifies how many songs of the history to return.
    """

    # Output format
    metrics = api.model('Metric over time', {
        'userid': fields.String,
        'metric_over_time': fields.Nested(api.model('metric', {
            'songid': fields.String,
            'name': fields.String,
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
            'valence': fields.Float,
            'excitedness': fields.Float,
            'happiness': fields.Float
        }))
    })

    @api.marshal_with(metrics, envelope='resource')
    def get(self, userid, song_count=0):
        """
        Obtain metrics and mood of a user for given number of songs.
        """
        _, _, songids = get_history(userid, song_count, return_songids=True, calc_mood=False)

        if songids:
            songs = models.Song.get_songs_with_mood(songids)
            songs_features = []

            for song, songmood in songs:
                features = song.__dict__
                for key in songmood.__dict__.keys():
                    features[key] = songmood.__dict__[key]
                songs_features.append(song.__dict__)

            if song_count != 0:
                songs_features = songs_features[:song_count]

            return {
                'userid': userid,
                'metric_over_time': songs_features
            }
        else:
            api.abort(404, message=f"No metrics found for '{userid}'")


# Output format for recommendationsong and recommendationmetric
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
class RecommendationSong(Resource):
    @api.marshal_with(recommendations, envelope='resource')
    def get(self, userid, songid, excitedness, happiness):
        """
        Obtain recommendations based on a song along with its excitedness and happiness.
        :param userid: Unique identifier for a user.
        :param songid: Unique identifier for a song.
        :param excitedness: Excitedness of the song specified by songid.
        :param happiness: happiness of the song specified by songid.
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
class RecommendationMetric(Resource):
    @api.marshal_with(recommendations, envelope='resource')
    def get(self, userid, metric):
        """
        Obtain recommendations based on an metric selected by user.
        """
        excitedness, happiness, songids = get_history(userid, 0, return_songids=True)
        recs = recommend_metric(songids[:6], userid, metric, excitedness, happiness)

        if recs:
            return {
                'userid': userid,
                'recommendations': recs
            }
        else:
            api.abort(404, message=f"No recommendations not found for '{userid}'")
