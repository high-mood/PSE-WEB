import os

# General settings
HOST = "localhost:5000"

# SQL settings
sql_user = "highmood_user"
sql_host = "localhost"
sql_database = "highmood"
sql_password = "password"

# Influx settings
INFLUX_USER = 'highmood'
INFLUX_PORT = 8086
INFLUX_HOST = "localhost"
INFLUX_PASSWORD = "password"

# Spotify settings
SPOTIFY_CLIENT = "client_key"
SPOTIFY_SECRET = "secret"

# Flask settings
DEBUG = False
WTF_CSRF_ENABLED = True
SECRET = "KLSDNFURWHFIUER87*HUSD"
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(sql_user, sql_password, sql_host, sql_database)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
ERROR_INCLUDE_MESSAGE = False
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
