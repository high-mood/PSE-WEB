# TODO: NOTE THAT THIS IS ONLY FOR DEVELOPMENT PURPOSES FILE SHOULD NOT BE INCLUDED WITHIN WEBSERVER

from influxdb import InfluxDBClient
import json
import sys


def total_time_spent(client, userid):
    """Return the cumulative time spent listening to songs paired per timestamp."""
    result = client.query('select cumulative_sum(duration_ms) from "' + userid + '"').raw
    cumsum = result['series'][0]['values']
    timestamp, listen_time = [list(x) for x in list(zip(*cumsum))]
    print(timestamp, listen_time)


def create_client(host, port):
    """Create the connection to the influxdatabase songs."""
    client = InfluxDBClient(host=host, port=port)
    client.switch_database('songs')
    return client


def get_genres(client, userid):
    """Return all genres listened to by the user."""
    result = client.query('select genres from "' + userid + '"').raw
    timestamps, genres = [list(x) for x in list(zip(*result['series'][0]['values']))]
    return timestamps, genres


def get_top(items, count):
    """Return the top items based on their occurrences."""
    items_count = [(item, items.count(item)) for item in items if item != 'None']
    top_items = sorted(set(count), key=lambda x: x[1], reverse=True)
    return top_items[:count]


def get_top_genres(client, userid, count):
    """Get the top 'count' genres of user"""
    genres = get_genres(client, userid)[1]
    print(get_top(genres, count))


def get_songs(client, userid):
    """Return all songs listened to by the user specified by userid."""
    result = client.query('select songid from "' + userid + '"').raw
    timestamp, songs = [list(x) for x in list(zip(*result['series'][0]['values']))]
    return timestamps, songs


def get_top_songs(client, userid, count):
    """Get the top 'count' songs of user"""
    songs = get_songs(client, userid)
    print(get_top(songs, count))


def main(argv):
    query = argv[1]
    userid = str(argv[2])
    client = create_client('localhost', 8086)
    total_time_spent(client, userid)

    if query == 'timespent':
        total_time_spent(client, userid)

    if len(argv) < 4:
        exit("""Usage: query.py <query> <userid> <count>
topsongs: get the top <count> songs, leave count empty for a default of 10
topgenres: get the top <count> genres, leave count empty for a default of 10""")

    count = argv[3]
    if query == 'topsongs':
        get_top_songs(client, userid, count)
    elif query == 'topgenres':
        get_top_genres(client, userid, count)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] == 'help':
        exit("""Usage: query.py <query> <userid> <count>
topsongs: get the top <count> songs, leave count empty for a default of 10
topgenres: get the top <count> genres, leave count empty for a default of 10
timespent: get the total time spent on spotify sampeled by timestamps of songs listened""")
    main(sys.argv)
