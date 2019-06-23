from influxdb import InfluxDBClient
from app.utils.models import Song
from app import app


def total_time_spent(client, userid):
    """
    Returns the cumulative time spent listening to songs paired per timestamp.
    :param client: InfluxDB client object.
    :param userid: User id of the user.
    :return: Cumulative time spent listening to songs paired per timestamp.
    """
    result = client.query('select cumulative_sum(duration_ms) from "' + userid + '"').raw

    if 'series' not in result:
        return None, 0

    cumsum = result['series'][0]['values']
    timestamp, listen_time = [list(x) for x in list(zip(*cumsum))]

    return timestamp, listen_time


def create_client(host, port):
    """
    Creates the connection to the influx database songs.
    :param host: Host ip of the InfluxDB.
    :param port: Host port of the InfluxDB.
    :return: Client object from the InfluxDB.
    """
    client = InfluxDBClient(host=host, port=port, username=app.config['INFLUX_USER'],
                            password=app.config['INFLUX_PASSWORD'], database='songs')

    return client


def get_genres(client, userid):
    """
    Returns all genres listened to by the user.
    :param client: InfluxDB client object.
    :param userid: User id of the user.
    :return: List of genres listened to by the user with there timestamps.
    """
    result = client.query('select genres from "' + userid + '"').raw

    if 'series' not in result:
        return 0,  []

    timestamps, genres = [list(x) for x in list(zip(*result['series'][0]['values']))]

    return timestamps, genres


def get_top(items, count):
    """
    Returns the top items based on their occurrences.
    :param items: List of items.
    :param count: Number of items to be returned.
    :return: The top items based on their occurrences.
    """

    if not items:
        return []

    items_count = [(item, items.count(item)) for item in items if item]
    top_items = sorted(set(items_count), key=lambda x: x[1], reverse=True)

    return top_items[:count]


def get_top_genres(client, userid, count):
    """
    Gets the top 'count' genres of user.
    :param client: InfluxDB client object.
    :param userid: User id of the user.
    :param count: Number of items to be returned.
    :return: The top genres of user.
    """
    genres = get_genres(client, userid)[1]

    return get_top(genres, count)


def get_songs(client, userid):
    """
    Returns all songs listened to by the user specified by userid.
    :param client: InfluxDB client object.
    :param userid: User id of the user.
    :return: All songs listened to by the user.
    """
    result = client.query('select songid from "' + userid + '"').raw

    if 'series' not in result:
        return 0, []

    timestamps, songs = [list(x) for x in list(zip(*result['series'][0]['values']))]

    songs = [Song.get_song_name(song) for song in songs]
    if all(song is None for song in songs):
        return 0, []

    return timestamps, songs


def get_top_songs(client, userid, count):
    """
    Gets the top 'count' songs of user
    :param client: InfluxDB client object.
    :param userid: User id of the user.
    :param count: Number of items to be returned.
    :return: The top songs of the user.
    """
    _, songs = get_songs(client, userid)

    return get_top(songs, count)
