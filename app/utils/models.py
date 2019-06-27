"""
    models.py
    ~~~~~~~~~~~~
    This file contains the structure of the sql database with functions to handle basic data flow.

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

import datetime

from app import db


class User(db.Model):
    """
    Database model for a user of the site.
    """
    __tablename__ = "users"
    userid = db.Column(db.String(200), primary_key=True)
    email = db.Column(db.String(200))
    display_name = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    birthdate = db.Column(db.DateTime(20))
    country = db.Column(db.String(5))
    is_premium = db.Column(db.Boolean(), default=False)
    refresh_token = db.Column(db.String(300))
    user_is_active = db.Column(db.Boolean())

    @staticmethod
    def create_if_not_exist(json_info, refresh_token):
        """
        Create a new user in the database if it does not yet exist.
        """
        user = User.query.filter_by(userid=json_info['id']).first()
        if user is None:
            user = User(userid=json_info['id'],
                        email=json_info['email'],
                        display_name=json_info['display_name'],
                        image_url=None,
                        birthdate=datetime.datetime.strptime(json_info['birthdate'], "%Y-%m-%d"),
                        country=json_info['country'],
                        is_premium=(json_info['product'] == "premium"),  # TODO this doens't work
                        refresh_token=refresh_token,
                        user_is_active=True)

            db.session.add(user)
            db.session.commit()

    @staticmethod
    def get_user(userid):
        """
        Get a user based on it's userid.
        :param userid: unique identifier for a user.
        :return: user object
        """
        return User.query.filter_by(userid=userid).first()

    @staticmethod
    def get_all_userids():
        """
        Return a list of all userids.
        """
        return [r.userid for r in db.session.query(User.userid)]

    @staticmethod
    def get_all_tokes():
        """Get a list of all refresh tokens."""
        return [r.refresh_token for r in db.session.query(User.refresh_token)]

    @staticmethod
    def get_refresh_token(userid):
        """
        Get the refresh token for user specified by userid.
        :param userid: unique identifier for a user.
        """
        return User.query.filter_by(userid=userid).first().refresh_token


class Song(db.Model):
    """
    Database model for a song, which stores all features.
    """
    __tablename__ = "songs"
    songid = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(300))
    duration_ms = db.Column(db.Float())
    key = db.Column(db.Float())
    mode = db.Column(db.Float())
    time_signature = db.Column(db.Float())
    acousticness = db.Column(db.Float())
    danceability = db.Column(db.Float())
    energy = db.Column(db.Float())
    instrumentalness = db.Column(db.Float())
    liveness = db.Column(db.Float())
    loudness = db.Column(db.Float())
    speechiness = db.Column(db.Float())
    valence = db.Column(db.Float())
    tempo = db.Column(db.Float())

    @staticmethod
    def create_if_not_exist(json_info):
        """
        Create a new song in the database if it does not already exist.
        :param json_info: dict of all features of a song object.
        """
        song = Song.query.filter_by(songid=json_info['songid']).first()
        if song is None:
            song = Song(songid=json_info['songid'],
                        name=json_info['name'],
                        duration_ms=json_info['duration_ms'],
                        key=json_info['key'],
                        mode=json_info['mode'],
                        time_signature=json_info['time_signature'],
                        acousticness=json_info['acousticness'],
                        danceability=json_info['danceability'],
                        energy=json_info['energy'],
                        instrumentalness=json_info['instrumentalness'],
                        liveness=json_info['liveness'],
                        loudness=json_info['loudness'],
                        speechiness=json_info['speechiness'],
                        valence=json_info['valence'],
                        tempo=json_info['tempo'])

            db.session.add(song)
            db.session.commit()

    @staticmethod
    def get_songs(songids):
        """
        Get all songs specified by songids.
        :param songids: list of unique identifier for songs.
        :return: list of song objects with songid in songids.
        """
        return Song.query.filter(Song.songid.in_(songids)).all()

    @staticmethod
    def get_song(songid):
        """
        Get a song specified by songid.
        :param songid: unique identifier for a song.
        :return: song object with songid.
        """
        return Song.query.filter_by(songid=songid).first()

    @staticmethod
    def get_song_name(songid):
        """
        Get name of a song specified by songid.
        :param songid: unique identifier for a song.
        :return: string name of song.
        """
        return Song.get_song(songid).name

    @staticmethod
    def get_songs_with_mood(songids):
        """
        Get the song and songmood objects specified by songids.
        :param songids: list of unique identifier for songs.
        :return: list of tuples(song, songmood)
        """
        return db.session.query(Songmood, Song).join(Song, Song.songid == Songmood.songid).filter(
            Song.songid.in_(songids)).all()

    @staticmethod
    def get_all_songs_with_mood_if_responses():
        """
        Get all song and songmood objects if a song has a response.
        :return: list of tuples(song, songmood)
        """
        return db.session.query(Songmood, Song).join(Song, Song.songid == Songmood.songid).filter(
            Songmood.response_count > 0).all()

    @staticmethod
    def get_all_songs_with_mood():
        """
        Get all song and songmood objects.
        :param songids: list of unique identifier for songs.
        :return: list of tuples(song, songmood)
        """
        return db.session.query(Songmood, Song).join(Song, Song.songid == Songmood.songid).all()


class Artist(db.Model):
    """
    Database model for artist, stores features for an artist
    """
    __tablename__ = "artists"
    artistid = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(300))
    genres = db.Column(db.String(300))
    popularity = db.Column(db.Integer())

    @staticmethod
    def create_if_not_exist(json_info):
        """
        Create an artist if it does not exist already.
        """
        artist = Artist.query.filter_by(artistid=json_info['artistid']).first()
        if artist is None:
            artist = Artist(artistid=json_info['artistid'],
                            name=json_info['name'],
                            genres=json_info['genres'],
                            popularity=json_info['popularity'])

            db.session.add(artist)
            db.session.commit()


class Songmood(db.Model):
    """
    Database model for songmood, stores mood for a given song.
    """
    __tablename__ = "songmoods"
    songid = db.Column(db.String(200), db.ForeignKey("songs.songid"), primary_key=True)
    excitedness = db.Column(db.Float())
    happiness = db.Column(db.Float())
    response_excitedness = db.Column(db.Float(), default=0.0)
    response_happiness = db.Column(db.Float(), default=0.0)
    response_count = db.Column(db.Integer(), db.ColumnDefault(0), default=0)

    @staticmethod
    def create_if_not_exist(json_info):
        """
        Create a songmood if it doesnt exist already.
        """
        songmood = Songmood.query.filter_by(songid=json_info['songid']).first()
        if songmood is None:
            songmood = Songmood(songid=json_info['songid'],
                                excitedness=json_info['excitedness'],
                                happiness=json_info['happiness'],
                                response_count=json_info['response_count'],
                                response_excitedness=json_info['response_excitedness'],
                                response_happiness=json_info['response_happiness'])

            db.session.add(songmood)
            db.session.commit()

    @staticmethod
    def get_moods(songids):
        """
        Get the songmoods specified by songids
        :param songids: list of unique identifier for song/songmood.
        :return: list of songmood objects.
        """
        return Songmood.query.filter(Songmood.songid.in_(songids)).all()

    @staticmethod
    def update_response_mood(songid, user_excitedness, user_happiness):
        """
        Update response mood with a user defined mood.
        :param songid: unique identifier for song/songmood.
        :param user_excitedness: user defined excitedness.
        :param user_happiness: user defined happiness.
        """
        songmood = Songmood.query.filter_by(songid=songid).first()
        if songmood:
            response_excitedness = songmood.response_excitedness
            response_happiness = songmood.response_happiness
            response_count = songmood.response_count
            songmood.response_happiness = (response_happiness * response_count + user_happiness) / (
                    response_count + 1)
            songmood.response_excitedness = (response_excitedness * response_count + user_excitedness) / (
                    1 + response_count)
            songmood.response_count = response_count + 1

            db.session.commit()


class SongArtist(db.Model):
    """
    Database model linking songs to artists.
    """
    __tablename__ = "songs_artists"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    songid = db.Column(db.String(200), db.ForeignKey("songs.songid"))
    artistid = db.Column(db.String(200), db.ForeignKey("artists.artistid"))

    __table_args__ = (db.UniqueConstraint('songid', 'artistid', name='key'),)

    @staticmethod
    def create_if_not_exist(json_info):
        """
        Create a link between a song and artist if it does not already exists.
        """
        song_artist = db.session.query(SongArtist).filter(SongArtist.songid == json_info['songid'],
                                                          SongArtist.artistid == json_info['artistid']).first()
        if song_artist is None:
            song_artist = SongArtist(songid=json_info['songid'],
                                     artistid=json_info['artistid'])

            db.session.add(song_artist)
            db.session.commit()
