from application import app
from flask import render_template

from .models import Cashier, Executive, Accounts, db, Transaction, Customer


@app.route("/")
def index():
    return render_template('index.html')