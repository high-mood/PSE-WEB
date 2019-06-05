import os

user = "username"
password = "password"
host = "host"
database = "databasename"
SECRET = "flask_secret"



WTF_CSRF_ENABLED = True
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(user,password,host,database)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')


SPOTIFY_SECRET = "SECRET"
SPOTIFY_CLIENT = "CLIENT"