from flask import Flask
import os

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd()) + "/test1.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

from application import models
from application import routes
from application import routes

app.static_folder = 'static'
