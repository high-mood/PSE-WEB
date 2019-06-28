"""
    user_calls.py
    ~~~~~~~~~~~~
    This file contains the structure of the user API with functions to handle basic GET and POST requests.

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

import datetime
from collections import defaultdict, Counter

import dateparser
from flask_restplus import Namespace, Resource, fields

from app import app
from app.utils import influx, models

api = Namespace('user', description='Information about user (over time)', path="/user")


@api.route('/info/<string:userid>')
@api.response(404, 'Userid not found')
class User(Resource):
    """
    Return all user info from the SQL database.
    """

    # Output format
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


def valid_hour(time, start_hour, end_hour):
    """
    Check if the time if correct.
    :param time: time in hours.
    :param start_hour: starting time in hours.
    :param end_hour: ending time in hours.
    :return: boolean specifying if time is valid.
    """

    mood_time = time.split(".")[0]
    mood_time = datetime.datetime.strptime(mood_time[:-1], '%Y-%m-%dT%H:%M:%S')
    mood_hour = mood_time.hour

    if start_hour <= mood_hour <= end_hour:
        return True
    return False


def convert_none(dicti):
    for key, value in dicti.items():
        if not value:
            dicti[key] = 0
    return dicti


@api.route('/mood/hourly/<string:userid>/<int:start>/<int:end>')
@api.response(400, 'Invalid date')
@api.response(404, 'No moods found')
class HourlyMood(Resource):
    """
    Return the hourly mood of a user specified within a timeframe. Thus over the entire history, we take the
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
        Obtain moods of a user within a given time frame as averages per hour.
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
                A = convert_none(A)
                # Now iterate over each song's metrics within the results and add the values using counter.
                for B in tempresults:
                    B = Counter(B)
                    B = convert_none(B)
                    try:
                        A = A + B
                    except TypeError:
                        count-=1

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


@api.route('/mood/daily/<string:userid>/<int:day_count>')
@api.response(400, 'Invalid date')
@api.response(404, 'No moods found')
class DailyMood(Resource):
    """
    Return the average metrics and mood per day for day_count number of days.
    """

    # Output format
    daily_mood = api.model('Mood over day', {
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

    @api.marshal_with(daily_mood, envelope='resource')
    def get(self=None, userid="snipy12", day_count=5):
        """
        Obtain average moods per day of user, going back day_count days.
        """

        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        songs = influx.get_songs(client, userid)

        if songs:
            # Create a dictionary of lists to store the songid's per hour
            # Thus {"Time":[songids,....]}
            resultDict = defaultdict(list)

            # For each {songid,time} in the list
            for song in songs:
                mood_time = song['time'].split(".")[0][:10]
                resultDict[mood_time].append(song['songid'])

            results = []
            # With the list of IDs with corresponding hour and features.
            for time, songid_list in list(resultDict.items())[:day_count]:
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
                A = convert_none(A)
                # Now iterate over each song's metrics within the results and add the values using counter.
                for B in tempresults:
                    B = Counter(B)
                    B = convert_none(B)
                    try:
                        A = A + B
                    except TypeError:
                        count -= 1

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
