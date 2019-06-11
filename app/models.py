# Imports here

from app import db
import datetime
"""smaple response:

{
  "display_name":"JMWizzler",
  "email":"email@example.com",
  "external_urls":{
  "spotify":"https://open.spotify.com/user/wizzler"
  },
  "href":"https://api.spotify.com/v1/users/wizzler",
  "id":"wizzler",
  "images":[{
  "height":null,
  "url":"https://fbcdn...2330_n.jpg",
  "width":null
  }],
  "product":"premium",
  "type":"user",
  "uri":"spotify:user:wizzler"
}"""


# TODO: Should user data be deleted after access revokeD?
# if not, boolean is active
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


class Song(db.Model):
    __tablename__ = "songs"
    songid = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(300))

    @staticmethod
    def create_if_not_exist(json_info):
        song = Song.query.filter_by(songid=json_info['songid']).first()
        if song is None:
            song = Song(songid=json_info['songid'],
                        name=json_info['name'])

            db.session.add(song)
            db.session.commit()


class Artist(db.Model):
    __tablename__ = "artists"
    artist_id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(300))
    genres = db.Column(db.String(300))
    popularity = db.Column(db.Integer())

    @staticmethod
    def create_if_not_exist(json_info):
        artist = Artist.query.filter_by(artist_id=json_info['artistid']).first()
        if artist is None:
            artist = Song(artist_id=json_info['artistid'],
                          name=json_info['name'],
                          genres=json_info['genres'],
                          popularity=json_info['popularity'])

            db.session.add(artist)
            db.session.commit()
