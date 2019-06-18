from flask_restplus import Namespace, Resource, fields
from app.utils import models

api = Namespace('user', description='User information', path="/user")

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


@api.route("/<string:userid>")
@api.response(404, 'Userid not found')
class User(Resource):
    @api.marshal_with(user_info, envelope='resource')
    def get(self, userid):
        """
        Obtain all of a user's account information.
        """
        user = models.User.query.filter_by(userid=userid).first()
        if not user:
            api.abort(404, msg="userid not found")

        return user
