from flask_restplus import Namespace, Resource, fields
from app.utils import influx, models
from app import app

api = Namespace('history', description='Song history', path="/history")

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


@api.route('/<string:userid>/<int:songcount>')
@api.response(404, 'No history found')
class History(Resource):
    @api.marshal_with(history, envelope='resource')
    def get(self, userid, songcount):
        """
        Obtain N most recently played songs along with their mood.
        """
        querycount = 3 * songcount
        client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
        recent_songs = client.query(f'select songid from "{userid}" order by time desc limit {querycount}')
        # print(recent_songs)
        if recent_songs:
            history = []
            recent_song_list = list(recent_songs.get_points(measurement=userid))
            songids = list(set([song['songid'] for song in recent_song_list]))
            songids = songids[:songcount] if songcount > 0 else songids
            songmoods = models.Songmood.get_moods(songids)
            excitedness = 0
            happiness = 0
            mean_count = 1

            for songmood in songmoods:
                if songmood.excitedness and songmood.happiness:
                    excitedness += songmood.excitedness
                    happiness += songmood.happiness
                    mean_count += 1 if mean_count != 1 else 0
                song = {}
                song['songid'] = songmood.songid
                song['excitedness'] = songmood.excitedness
                song['happiness'] = songmood.happiness
                song['time'] = [song['time'] for song in recent_song_list][0]
                song['name'] = models.Song.get_song_name(song['songid'])
                history.append(song)
            excitedness /= mean_count
            happiness /= mean_count

            return {
                'userid': userid,
                'mean_excitedness': excitedness,
                'mean_happiness': happiness,
                'songs': history
            }
        else:
            api.abort(404, msg=f"No history not found for '{userid}'")
