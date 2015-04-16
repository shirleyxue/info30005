import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir

app = Flask(__name__) # initialise app!
app.config.from_object('config') # import config
db = SQLAlchemy(app) # initialise db!

lm = LoginManager() # create login manager object
lm.init_app(app)
lm.login_view = 'login' # tell flask which view handles login

from app import views, models
