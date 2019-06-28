"""
    influx.py
    ~~~~~~~~~~~~
    This file contains functions for the data flow with the influx database.

    :copyright: 2019 Moodify (High-Mood)
    :authors:
           "Stan van den Broek",
           "Mitchell van den Bulk",
           "Mo Diallo",
           "Arthur van Eeden",
           "Elijah Erven",
           "Henok Ghebrenigus",
           "Jonas van der Ham",
           "Mounir El Kirafi",
           "Esmeralda Knaap",
           "Youri Reijne",
           "Siwa Sardjoemissier",
           "Barry de Vries",
           "Jelle Witsen Elias"
"""

from influxdb import InfluxDBClient

from app import app


def create_client(host, port, database='songs'):
    """
    Creates the connection to the influx database songs.
    :param host: Host ip of the InfluxDB.
    :param port: Host port of the InfluxDB.
    :param database: database to use.
    :return: Client object from the InfluxDB.
    """
    client = InfluxDBClient(host=host, port=port, username=app.config['INFLUX_USER'],
                            password=app.config['INFLUX_PASSWORD'], database=database)

    return client


def get_mood(client, userid):
    client.switch_database('moods')

    return client.query(f'select excitedness, happiness, songcount from "{userid}"')


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


def get_songs(client, userid, limit=None, duration=None):
    """
    Returns songs listened to by the user specified by userid.
    :param client: InfluxDB client object.
    :param userid: User id of the user.
    :param limit: Limits the number of songs to be returned.
    :param duration: Limits the time frame from where the songs are returned.
    :return: All songs listened to by the user.
    """
    if limit == 0:
        limit = None

    filters = ""
    if duration:
        filters += f" where time > now()-{duration}"
    filters += " order by time desc"
    if limit:
        filters += f" limit {limit}"

    result = client.query(f'select songid from "{userid}"{filters}')

    if not result:
        return []

    return list(result.get_points(measurement=userid))


def get_top_songs(client, userid, count):
    """
    Gets the top 'count' songs of user
    :param client: InfluxDB client object.
    :param userid: User id of the user.
    :param count: Number of items to be returned.
    :return: The top songs of the user.
    """
    songs = get_songs(client, userid)

    return get_top([song['songid'] for song in songs], count)
