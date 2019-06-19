from app import db
import datetime


class User(db.Model):
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
        user = User.query.filter_by(userid=json_info['id']).first()
        if user is None:
            user = User(userid=json_info['id'],
                        email=json_info['email'],
                        display_name=json_info['display_name'],
                        image_url=None,
                        birthdate=datetime.datetime.strptime(json_info['birthdate'], "%Y-%m-%d"),
                        country=json_info['country'],
                        is_premium=(json_info['product'] is "premium"),  # TODO this doens't work
                        refresh_token=refresh_token,
                        user_is_active=True)

            db.session.add(user)
            db.session.commit()

    @staticmethod
    def get_all_tokes():
        query = db.session.query("refresh_token FROM users")
        return [row[0] for row in query]

    @staticmethod
    def get_all_users():
        query = db.session.query("userid FROM users")
        return [row[0] for row in query]

    @staticmethod
    def get_refresh_token(userid):
        query = db.session.query(f"refresh_token FROM users where userid='{userid}'")
        return query[0][0]


class Song(db.Model):
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
    def get_song_name(songid):
        song = Song.query.filter_by(songid=songid).first()
        return song.name


class Artist(db.Model):
    __tablename__ = "artists"
    artistid = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(300))
    genres = db.Column(db.String(300))
    popularity = db.Column(db.Integer())

    @staticmethod
    def create_if_not_exist(json_info):
        artist = Artist.query.filter_by(artistid=json_info['artistid']).first()
        if artist is None:
            artist = Artist(artistid=json_info['artistid'],
                            name=json_info['name'],
                            genres=json_info['genres'],
                            popularity=json_info['popularity'])

            db.session.add(artist)
            db.session.commit()


class Songmood(db.Model):
    __tablename__ = "songmoods"
    songid = db.Column(db.String(200), db.ForeignKey("songs.songid"), primary_key=True)
    excitedness = db.Column(db.Float())
    happiness = db.Column(db.Float())
    responses_count = db.Column(db.Integer(), db.ColumnDefault(50))

    @staticmethod
    def create_if_not_exist(json_info):
        songmood = Songmood.query.filter_by(songid=json_info['songid']).first()
        if songmood is None:
            songmood = Songmood(songid=json_info['songid'],
                                excitedness=json_info['excitedness'],
                                happiness=json_info['happiness'])

            db.session.add(songmood)
            db.session.commit()

    @staticmethod
    def get_moods(songids):
        songmoods = db.session.query(Songmood).filter(Songmood.songid.in_((songids))).all()
        return songmoods


class SongArtist(db.Model):
    __tablename__ = "songs_artists"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    songid = db.Column(db.String(200), db.ForeignKey("songs.songid"))
    artistid = db.Column(db.String(200), db.ForeignKey("artists.artistid"))

    __table_args__ = (db.UniqueConstraint('songid', 'artistid', name='key'),)

    @staticmethod
    def create_if_not_exist(json_info):
        songartist = SongArtist.query(f"select id from songs_artists where songid={songid} and artistid={artistid}").first()
        if songartist is None:
            songartist = SongArtist(songid=json_info['songid'],
                                    artistid=json_info['artistid'])

            db.session.add(songartist)

            db.session.commit()
