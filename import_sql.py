from app import db
from app.API import spotify, influx
from app import app
import numpy as np
from app.models import Song


client = influx.create_client(app.config['INFLUX_HOST'], app.config['INFLUX_PORT'])
client.switch_database('songs')
all_data = client.query('select "acousticness", "danceability", "duration_ms", "energy", "instrumentalness", "key", "liveness", "loudness", "mode", "songid", "speechiness", "tempo", "time_signature", "valence"  from /.*/').raw['series']
all_values = [data['values'] for data in all_data]
columns = all_data[0]['columns']
flattened_data = [x for sublist in all_values for x in sublist]
data_dict = [{name: val  for name, val in list(zip(columns, data)) if name != 'time'} for data in flattened_data]
for data in data_dict:
    Song.query.filter_by(songid=data['songid']).update(data)
db.session.commit()

