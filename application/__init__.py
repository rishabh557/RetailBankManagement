from flask import Flask
import os

app = Flask(__name__)
app.secret_key = "super secret key"
file_path = os.path.abspath(os.getcwd()) + "/test1.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from application import models
from application import routes
from application import routes

app.static_folder = 'static'
