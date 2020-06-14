from application import app
from flask import render_template

from .models import Cashier, Executive, Accounts, db, Transaction, Customer

from flask import Flask, render_template, redirect, url_for

@app.route('/home')
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/executivelogin')
def executivelogin():
    return render_template('executivelogin.html')

@app.route('/cashierlogin')
def cashierlogin():
    return render_template('cashierlogin.html')

@app.route('/executivehome')
def executivehome():
    return render_template('executivehome.html')

@app.route('/cashierhome')
def executivecashier():
    return render_template('cashierhome.html')