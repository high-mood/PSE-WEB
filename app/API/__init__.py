# TODO: restructur this code
# TODO: unit tests
import datetime
import json

from . import views
from app import app
from flask_restplus import Api, Resource, fields
from flask import Blueprint, jsonify
from app import models

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)

user_name_space = api.namespace('user', description='User information', path="user")

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


user_statistics = api.model('User Statistics', {
    'userid': fields.String,
    'username': fields.String,
    'mean_excitedness': fields.String,
    'mean_happiness': fields.String,
    'songs': fields.Nested(api.model('song', {
        'songname': fields.String,
        'timestamp': fields.Integer,
        'excitedness': fields.Integer,
        'happiness': fields.Integer
    }))

})


@user_name_space.route('statistics/<string:userid>')
class BasicUserData(Resource):
    @api.marshal_with(user_statistics, envelope='resource')
    def get(self, userid):
        """
        Obtain basic aggregated statistics for a user.
        """
        # TODO: CHANGE THIS
        from resources import query
        client = query.create_client('pse-ssh.diallom.com', 8086)

        user = models.User.query.filter_by(userid=userid).first()
        from app.API.spotify import get_access_token
        songs = query.get_songs(client, userid, get_access_token(user.refresh_token))
        print(songs)

        return {
            'userid': userid,
            'username': user.display_name,
            # 'mean_excitedness': fields.String,
            # 'mean_happiness': fields.String,
            # 'songs': fields.Nested(api.model('song', {
            #     'songname': fields.String,
            #     'timestamp': fields.Integer,
            #     'excitedness': fields.Integer,
            #     'happiness': fields.Integer
            # }))

        }

# def post(self):
#     return {
#         "status": "Posted new data"
#     }
