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

name_space = api.namespace('User', description='User information')

model = api.model('UserInfo', {
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


@name_space.route("/<string:userid>")
class MoodData(Resource):

    @api.marshal_with(model, envelope='resource')
    def get(self, userid):
        """
        Obtain all of a user's account information.
        """

        user = models.User.query.filter_by(userid=userid).first()
        return user
# def post(self):
#     return {
#         "status": "Posted new data"
#     }


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)
