from app.utils.exceptions import NoResultsFound, InvalidValue
from flask_restplus import Api
from flask import Blueprint
from app import app

from .users import api as user_name_space
from .tracks import api as track_name_space

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)

api.add_namespace(user_name_space)
api.add_namespace(track_name_space)


@api.errorhandler
def default_error_handler(error):
    """ Default error handler. """
    if not app.config['DEBUG']:
        return {'message': 'An unhandled exception occurred.'}, getattr(error, 'code', 500)


@api.errorhandler(InvalidValue)
@api.errorhandler(NoResultsFound)
def error_handler(error):
    return {'message': str(error['msg'])}, error['code']
