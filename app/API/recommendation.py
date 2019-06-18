from flask_restplus import Namespace, Resource, fields
from app.utils.tasks import find_song_recommendations
from app.utils import influx
from app import app

api = Namespace('recommendation', description='Song recommendations', path="/recommendation")

recommendations = api.model('Song recommendations', {
    'userid': fields.String,
    'recommendations': fields.Nested(api.model('recommendation', {
        'songid': fields.String,
        'song_url': fields.String,
        'artists': fields.List(fields.String),
        'name': fields.String,
        'image_url': fields.String
    }))
})


@api.route('<string:userid>/<int:recommendation_count>')
@api.response(404, 'No recommendations found')
class Recommendation(Resource):
    @api.marshal_with(recommendations, envelope='resource')
    def get(self, userid, recommendation_count):
        """
        Obtain {recommendation_count} recommendations for user {userid} along
        with their features.
        """
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc limit 5')
        if recent_songs:
            recent_songs = list(recent_songs.get_points(measurement=userid))
            songids = [song['songid'] for song in recent_songs]
            recs = find_song_recommendations(songids, userid, recommendation_count)
            if recs:
                return {
                    'userid': userid,
                    'recommendations': recs
                }
            else:
                api.abort(404, msg=f"No recommendations not found for '{userid}'")
