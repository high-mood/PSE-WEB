from collections import defaultdict, Counter

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


# It should return Should
@api.route('/mood/<string:userid>/<int:start>/<int:end>')
@api.response(400, 'Invalid date')
@api.response(404, 'No moods found')
class Mood(Resource):
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


#################################################################################################################
def valid_hour(time, start_hour, end_hour):
    """

    :param time:
    :param start_hour:
    :param end_hour:
    :return:
    """

    mood_time = time.split(".")[0]
    mood_time = datetime.datetime.strptime(mood_time[:-1], '%Y-%m-%dT%H:%M:%S')
    mood_hour = mood_time.hour

    if start_hour <= mood_hour <= end_hour:
        return True
    return False


@api.route('/mood/hourly/<string:userid>/<int:start>/<int:end>')
@api.response(400, 'Invalid date')
@api.response(404, 'No moods found')
class HourlyMood(Resource):
    """
    This API returns the hourly mood of a user specified within a timeframe. Thus over the entire history, we take the
    average for each hour within the specified hourly timeframe.
    """

    # Output format
    hourly_mood = api.model('Mood over hour', {
        'userid': fields.String,
        'hours': fields.Nested(api.model('metrics_mood', {
            "hour": fields.String,
            "excitedness": fields.Float,
            "happiness": fields.Float,
            "acousticness": fields.Float,
            "danceability": fields.Float,
            "duration_ms": fields.Float,
            "energy": fields.Float,
            "instrumentalness": fields.Float,
            "key": fields.Float,
            "liveness": fields.Float,
            "loudness": fields.Float,
            "mode": fields.Float,
            "speechiness": fields.Float,
            "tempo": fields.Float,
            "valence": fields.Float
        }))
    })

    @api.marshal_with(hourly_mood, envelope='resource')
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
        songs = influx.get_songs(client, userid)

        if songs:
            # Extract all songs that fit within the time-frame specified.
            relevantSongs = [val for val in songs if valid_hour(val['time'], start, end)]

            # Create a dictionary of lists to store the songid's per hour
            # Thus {"Time":[songids,....]}
            resultDict = defaultdict(list)

            # For each {songid,time} in the list
            for song in relevantSongs:
                mood_time = song['time'].split(".")[0]
                mood_time = datetime.datetime.strptime(mood_time[:-1], '%Y-%m-%dT%H:%M:%S')
                mood_hour = mood_time.hour

                # TODO: This is always true so duplicate code
                if start <= mood_hour <= end:
                    # Add the songid to the dictionary
                    resultDict[mood_hour].append(song['songid'])

            results = []
            # With the list of IDs with corresponding hour and features.
            for time, songid_list in resultDict.items():
                # Obtain the metrics for each song inside a list of songs.
                songs = models.Song.get_songs_with_mood(songid_list)

                tempresults = []

                for song in songs:
                    # We want both the mood and metrics thus we convert the object to a dictionary and combine them
                    # Then we pop the keys of said dictionary.
                    temp1 = ((song[0].__dict__))
                    temp2 = ((song[1].__dict__))
                    combineddict = {**temp1, **temp2}
                    combineddict.pop("name")
                    combineddict.pop("_sa_instance_state")
                    combineddict.pop("songid")

                    # Add the metrics of a SINGLE song to the temporary result
                    tempresults.append(combineddict)

                # As we are interested in the average we store the count of this list
                count = len(tempresults)
                # Remove the first element, which will be used for addition
                A = Counter(tempresults.pop(0))
                # Now iterate over each song's metrics within the results and add the values using counter.
                for B in tempresults:
                    B = Counter(B)
                    A = A + B

                # Convert these to averages by dividing each key if possible
                for key, value in A.items():
                    if value:
                        A[key] = value / count
                    else:
                        A[key] = 0

                # Add hour key for correct output format and append to results
                A['hour'] = time
                results.append(A)

            return {"userid": userid,
                    "hours": results}

        else:
            api.abort(404, msg=f"No moods found for '{userid}'")







@api.route('/mood/hourly/<string:userid>/<int:duration>')
@api.response(400, 'Invalid date')
@api.response(404, 'No moods found')
class DailyMood(Resource):
    """
    This API returns the hourly mood of a user specified within a timeframe. Thus over the entire history, we take the
    average for each hour within the specified daily timeframe.
    """

    # Output format
    hourly_mood = api.model('Mood over day', {
        'userid': fields.String,
        'dates': fields.Nested(api.model('metrics_mood', {
            "date": fields.String,
            "excitedness": fields.Float,
            "happiness": fields.Float,
            "acousticness": fields.Float,
            "danceability": fields.Float,
            "duration_ms": fields.Float,
            "energy": fields.Float,
            "instrumentalness": fields.Float,
            "key": fields.Float,
            "liveness": fields.Float,
            "loudness": fields.Float,
            "mode": fields.Float,
            "speechiness": fields.Float,
            "tempo": fields.Float,
            "valence": fields.Float
        }))
    })

    @api.marshal_with(hourly_mood, envelope='resource')
    def get(self=None, userid="snipy12", duration=5):
        """
        Obtain moods of a user within a given time frame in hours of a day.
        """



        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        songs = influx.get_songs(client, userid)

        if songs:


            # Create a dictionary of lists to store the songid's per hour
            # Thus {"Time":[songids,....]}
            resultDict = defaultdict(list)

            # For each {songid,time} in the list
            for song in songs:
                mood_time = song['time'].split(".")[0]
                mood_time = datetime.datetime.strptime(mood_time[:-1], '%Y-%m-%dT%H:%M:%S')

                resultDict[mood_time.day].append(song['songid'])

            results = []
            # With the list of IDs with corresponding hour and features.
            for time, songid_list in resultDict.items():
                # Obtain the metrics for each song inside a list of songs.
                songs = models.Song.get_songs_with_mood(songid_list)

                tempresults = []

                for song in songs:
                    # We want both the mood and metrics thus we convert the object to a dictionary and combine them
                    # Then we pop the keys of said dictionary.
                    temp1 = ((song[0].__dict__))
                    temp2 = ((song[1].__dict__))
                    combineddict = {**temp1, **temp2}
                    combineddict.pop("name")
                    combineddict.pop("_sa_instance_state")
                    combineddict.pop("songid")

                    # Add the metrics of a SINGLE song to the temporary result
                    tempresults.append(combineddict)

                # As we are interested in the average we store the count of this list
                count = len(tempresults)
                # Remove the first element, which will be used for addition
                A = Counter(tempresults.pop(0))
                # Now iterate over each song's metrics within the results and add the values using counter.
                for B in tempresults:
                    # TODO DO THIS EVERYWHERE ALSO OTHER API CALL
                    B = Counter(B)
                    for key, value in B.items():
                        if not value:
                            B[key] = 0

                    A = A + B

                # Convert these to averages by dividing each key if possible
                for key, value in A.items():
                    if value:
                        A[key] = value / count
                    else:
                        A[key] = 0

                # Add hour key for correct output format and append to results
                A['date'] = time
                results.append(A)

            return {"userid": userid,
                    "dates": results}

        else:
            api.abort(404, msg=f"No moods found for '{userid}'")



