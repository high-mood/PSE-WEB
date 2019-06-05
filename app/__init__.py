import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.environ.get("APP_SECRET", "HELLO") # THIS SHOULD BE SOMETHING RANDOM
db = SQLAlchemy(app)
from app import views


