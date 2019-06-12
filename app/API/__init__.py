import datetime
import json

from . import views
from app import app
from flask_restplus import Api, Resource
from flask import Blueprint, jsonify
from app import models

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)

name_space = api.namespace('Users', description='Main APIs')


@name_space.route("/<string:id>")
class Users(Resource):

    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the person'})
    def get(self,id):
        us = models.User.query.filter_by(userid=id).first().__dict__
        us.pop('_sa_instance_state', None)


        return json.dumps(us,cls=DateTimeEncoder)
    def post(self):
        return {
            "status": "Posted new data"
        }


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)
