# TODO: restructur this code
# TODO: unit tests
import datetime
import json

from . import views
from app import app
from flask_restplus import Api, Resource, fields
from flask import Blueprint, jsonify
from app import models

from influxdb import InfluxDBClient
import config
import numpy as np

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)

user_name_space = api.namespace('user', description='User information', path="/user")
mood_name_space = api.namespace('mood', description='Mood over time', path="/mood")

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
            'songcount' : fields.Integer
        }))
    })


@mood_name_space.route('/<string:userid>/<string:start>/<string:end>')
class Mood(Resource):
    @api.marshal_with(moods, envelope='resource')
    def get(self, userid, start="'1678-09-21T00:20:43.145224194Z'",
            end=str("'" + datetime.datetime.now().isoformat() + "Z'")):
        """
        Obtain moods of a user within a given timeframe. Append '/' after every parameter.
        """
        print('===========================================')
        print(userid, start, end)

        if start == '0' or 'begin' or 'beginning of time':
            start = "'1678-09-21T00:20:43.145224194Z'"

        if end == 'now':
            end = str("'" + datetime.datetime.now().isoformat() + "Z'")

        print(start, end)
        client = InfluxDBClient(host='pse-ssh.diallom.com', port=8086, username=config.influx_usr,
                                password=config.influx_pswd, database='moods')
        moods = client.query(f"select excitedness, happiness, songcount from {userid} where time > {start} and time < {end}")
        moodlist = list(moods.get_points(measurement=userid))

        v = [[mood['excitedness'], mood['happiness'], mood['songcount']] for mood in moodlist]
        mean_happiness, mean_excitedness, _ = np.mean(v, axis=0)
        _, _, sum_song_count = np.sum(v, axis=0)

        if moods:
            return {
                'userid': userid,
                'mean_excitedness': mean_excitedness,
                'mean_happiness': mean_happiness,
                'sum_song_count': sum_song_count,
                'moods': moodlist
            }
