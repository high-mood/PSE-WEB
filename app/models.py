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
    user_id = db.Column(db.String(200),primary_key=True)
    email = db.Column(db.String(200))
    display_name = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    birthdate = db.Column(db.DateTime(20))
    country = db.Column(db.String(5))
    is_premium = db.Column(db.Boolean(),default=False)
    refresh_token = db.Column(db.String(300))
    user_is_active = db.Column(db.Boolean())

    @staticmethod
    def create_if_not_exist(json_info, refresh_token):
        user = User.query.filter_by(user_id=json_info['id']).first()
        if user is None:
            user = User(user_id=json_info['id'],
                        email=json_info['email'],
                        display_name=json_info['display_name'],
                        image_url=None,
                        birthdate=datetime.datetime.strptime(json_info['birthdate'], "%Y-%m-%d"),
                        country=json_info['country'],
                        is_premium=(json_info['product'] is "premium"),
                        refresh_token=refresh_token,
                        user_is_active=True)

            db.session.add(user)
            db.session.commit()
