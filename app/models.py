# Imports here

from app import db

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


class User(db.Model):
    user_id = db.Column(db.String(200),primary_key=True)
    email = db.Column(db.String(200))
    display_name = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    birthdate = db.Column(db.DateTime(20))
    country = db.Column(db.String(5))
    is_premium = db.Column(db.Boolean(),default=False)
    refresh_token = db.Column(db.String(300))